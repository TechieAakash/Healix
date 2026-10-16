"""
Central AI Orchestrator for Healix.
Manages the end-to-end clinical workflow:
Sanitization -> Extraction -> Deterministic Safety -> RAG -> LLM Reasoning ->
Grounding Check -> Safety Validation -> Response Building -> Observability Tracking.
"""

import json
import logging
import time
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.utils.constants import UrgencyLevel, STANDARD_MEDICAL_DISCLAIMER
from app.services.ai.llm.base import BaseLLMProvider
from app.services.ai.llm.provider import get_llm_provider
from app.services.ai.symptom_extractor import SymptomExtractor
from app.services.ai.follow_up_engine import FollowUpQuestionEngine
from app.services.ai.rag.retriever import RAGRetriever
from app.services.ai.safety.sanitizer import ContextSanitizer
from app.services.ai.safety.grounding import GroundingValidator
from app.services.ai.safety.validator import ClinicalSafetyValidator
from app.services.ai.observability.tracker import ai_tracker
from app.services.ai.schemas import (
    SymptomAnalysisResponse,
    HealthSummaryResponse,
    PossibleExplanationItem,
    SourceCitation,
)
from app.services.ai.prompts.symptom_analysis import (
    ANALYSIS_SYSTEM_PROMPT,
    ANALYSIS_USER_PROMPT_TEMPLATE,
)
from app.services.ai.prompts.summary import (
    SUMMARY_SYSTEM_PROMPT,
    SUMMARY_USER_PROMPT_TEMPLATE,
)
from app.services.ai.prompts.chat import (
    CHAT_SYSTEM_PROMPT,
    CHAT_USER_PROMPT_TEMPLATE,
)
from app.services.triage_service import TriageService
from app.services.ai_service import AIService

logger = logging.getLogger("healix.ai.orchestrator")


class AIOrchestrator(AIService):
    """
    Production-grade AI Orchestrator implementing the full Healix AI pipeline.
    Maintains independence of the deterministic safety engine and guarantees
    that LLMs can never override emergency triage classifications.
    """

    def __init__(
        self,
        llm_provider: Optional[BaseLLMProvider] = None,
        retriever: Optional[RAGRetriever] = None,
        triage_service: Optional[TriageService] = None,
    ):
        self.llm = llm_provider or get_llm_provider()
        self.retriever = retriever or RAGRetriever()
        self.triage = triage_service or TriageService()
        self.extractor = SymptomExtractor(self.llm)
        self.follow_up_engine = FollowUpQuestionEngine(self.llm)

    async def extract_symptoms(self, description: str) -> Dict[str, Any]:
        """
        Step 1 & 2: Sanitize input and extract structured symptoms.
        """
        start = time.perf_counter()
        sanitized_input = ContextSanitizer.sanitize_text(description)
        sanitized_input = ContextSanitizer.inspect_and_neutralize_prompt_injection(sanitized_input)

        extracted = await self.extractor.extract_and_normalize(sanitized_input)
        latency = (time.perf_counter() - start) * 1000

        ai_tracker.record(
            operation_type="symptom_extraction",
            latency_ms=latency,
            retrieval_count=0,
            validation_status="SUCCESS",
        )
        return extracted

    async def generate_follow_up_questions(
        self,
        description: str,
        symptoms: List[Dict[str, Any]],
        previous_answers: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Step 3: Generate context-dependent, short, clinically targeted questions.
        """
        start = time.perf_counter()
        sanitized_desc = ContextSanitizer.sanitize_text(description)
        sanitized_desc = ContextSanitizer.inspect_and_neutralize_prompt_injection(sanitized_desc)

        # Pre-check deterministic safety before generating questions
        triage_pre = self.triage.evaluate(
            description=sanitized_desc,
            symptoms=symptoms,
            answers=previous_answers or [],
        )

        # If already an acute emergency, ask safety confirmation question first
        if triage_pre["urgency_level"] == UrgencyLevel.EMERGENCY.value:
            questions = [
                {
                    "question": "Are you able to immediately contact emergency medical services (911 / 112) or reach an emergency room?",
                    "type": "single_choice",
                    "order_index": 0,
                    "reasoning": "Immediate patient safety confirmation for acute emergency signs.",
                    "options": ["Yes, contacting emergency services", "Need assistance reaching care"],
                }
            ]
        else:
            questions = await self.follow_up_engine.generate_questions(
                description=sanitized_desc,
                symptoms=symptoms,
                previous_answers=previous_answers,
            )

        latency = (time.perf_counter() - start) * 1000
        ai_tracker.record(
            operation_type="follow_up_questions",
            latency_ms=latency,
            retrieval_count=0,
            validation_status="SUCCESS",
        )
        return questions

    async def analyze_symptoms(
        self, description: str, symptoms: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Backwards-compatible AIService method. Delegates to RAG-augmented analysis.
        """
        triage_result = self.triage.evaluate(description=description, symptoms=symptoms)
        return await self.generate_summary(
            description=description,
            symptoms=symptoms,
            answers=[],
            triage_result=triage_result,
        )

    async def generate_summary(
        self,
        description: str,
        symptoms: List[Dict[str, Any]],
        answers: List[Dict[str, Any]],
        triage_result: Dict[str, Any],
        assessment_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Step 4 to 9: Complete Analysis, RAG, Reasoning, Grounding, and Safety Pipeline.
        """
        start_time = time.perf_counter()
        deterministic_urgency = triage_result.get("urgency_level", UrgencyLevel.ROUTINE.value)

        # 1. PII and Context Sanitization
        clean_desc = ContextSanitizer.sanitize_text(description)
        clean_desc = ContextSanitizer.inspect_and_neutralize_prompt_injection(clean_desc)
        clean_symptoms = [ContextSanitizer.sanitize_context_data(s) for s in symptoms]
        clean_answers = [ContextSanitizer.sanitize_context_data(a) for a in answers]

        # 2. RED-FLAG HARD SAFETY BOUNDARY CHECK
        # If deterministic triage flagged EMERGENCY, bypass normal casual generation!
        if deterministic_urgency == UrgencyLevel.EMERGENCY.value:
            logger.warning("Deterministic emergency rule triggered! Enforcing hard safety boundary.")
            emergency_summary = self._build_emergency_fallback_response(
                clean_desc, clean_symptoms, triage_result
            )
            latency = (time.perf_counter() - start_time) * 1000
            ai_tracker.record(
                operation_type="emergency_safety_enforced",
                latency_ms=latency,
                assessment_id=assessment_id,
                retrieval_count=0,
                validation_status="EMERGENCY_ENFORCED",
                fallback_used=False,
            )
            return emergency_summary

        # 3. RAG Retrieval & Source Preservation
        query_terms = [clean_desc] + [s.get("name", "") for s in clean_symptoms]
        search_query = " ".join([q for q in query_terms if q]).strip() or "general health inquiry"

        retrieved_chunks = await self.retriever.retrieve_context(search_query)
        rag_context_block = self.retriever.build_rag_context_block(retrieved_chunks)
        citations = self.retriever.format_citations(retrieved_chunks)
        doc_ids = [chk.get("document_id", "DOC_UNKNOWN") for chk in retrieved_chunks]

        # 4. LLM Reasoning / Structured Output Generation
        analysis_prompt = ANALYSIS_USER_PROMPT_TEMPLATE.format(
            description=clean_desc,
            symptoms_json=json.dumps(clean_symptoms, indent=2),
            answers_json=json.dumps(clean_answers, indent=2),
            urgency_level=deterministic_urgency,
            rag_context=rag_context_block,
        )

        analysis_obj: Optional[SymptomAnalysisResponse] = None
        fallback_used = False
        error_type = None

        try:
            analysis_obj = await self.llm.generate_structured(
                schema=SymptomAnalysisResponse,
                prompt=analysis_prompt,
                system_prompt=ANALYSIS_SYSTEM_PROMPT,
                temperature=settings.AI_TEMPERATURE,
                max_retries=settings.AI_MAX_RETRIES,
            )
        except Exception as exc:
            logger.error("LLM structured analysis failed: %s. Engaging safe fallback.", str(exc))
            fallback_used = True
            error_type = type(exc).__name__
            analysis_obj = self._build_safe_fallback_analysis(clean_symptoms, deterministic_urgency)

        # 5. Grounding & Hallucination Check
        full_analysis_text = " ".join(
            [e.description for e in analysis_obj.possible_explanations]
            + analysis_obj.warning_signs
            + analysis_obj.general_guidance
        )
        grounding_result = GroundingValidator.evaluate_grounding(full_analysis_text, retrieved_chunks)

        # 6. Response Building
        symptom_titles = ", ".join([s.get("name", "") for s in clean_symptoms]) or "Reported Symptoms"
        narrative_summary = (
            f"Health assessment review for: {symptom_titles}. "
            f"Safety evaluation level: {deterministic_urgency}. "
            f"{triage_result.get('message', '')}"
        )

        raw_result = {
            "summary": narrative_summary,
            "urgency_level": deterministic_urgency,
            "possible_explanations": [e.model_dump() for e in analysis_obj.possible_explanations],
            "general_guidance": analysis_obj.general_guidance,
            "warning_signs": analysis_obj.warning_signs,
            "sources": citations if citations else self._default_authoritative_sources(),
            "disclaimer": STANDARD_MEDICAL_DISCLAIMER,
        }

        # 7. Final Safety Validation Layer (Prohibitions, Certainty Sanitization, Emergency Non-Downgrade)
        validated_result = ClinicalSafetyValidator.validate_and_sanitize_response(
            raw_result, deterministic_urgency=deterministic_urgency
        )

        # 8. Observability & Audit Trail Recording
        latency = (time.perf_counter() - start_time) * 1000
        ai_tracker.record(
            operation_type="assessment_analysis",
            latency_ms=latency,
            assessment_id=assessment_id,
            retrieval_count=len(retrieved_chunks),
            retrieved_document_ids=doc_ids,
            validation_status="GROUNDING_FLAGGED" if not grounding_result.is_grounded else ("FALLBACK" if fallback_used else "SUCCESS"),
            fallback_used=fallback_used,
            error_type=error_type,
        )

        return validated_result

    async def chat(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        assessment_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Step 13: Context-Aware Chatbot with sliding window history and RAG grounding.
        """
        start = time.perf_counter()

        # Sanitize user query
        clean_user_msg = ContextSanitizer.sanitize_text(user_message)
        clean_user_msg = ContextSanitizer.inspect_and_neutralize_prompt_injection(clean_user_msg)

        # Context Window Management: sliding window of last 6 messages
        recent_history = conversation_history[-6:]
        history_formatted = "\n".join([
            f"{m.get('role', 'user').upper()}: {m.get('content', '')}"
            for m in recent_history
        ])

        # RAG retrieval for specific question
        retrieved_chunks = await self.retriever.retrieve_context(clean_user_msg, top_k=2)
        rag_context_block = self.retriever.build_rag_context_block(retrieved_chunks)

        # Assessment context snapshot
        assessment_snapshot = "No active assessment attached."
        if assessment_context:
            assessment_snapshot = (
                f"Urgency Level: {assessment_context.get('urgency_level', 'UNKNOWN')}\n"
                f"Primary Summary: {assessment_context.get('summary', 'None')}"
            )

        chat_prompt = CHAT_USER_PROMPT_TEMPLATE.format(
            assessment_context=assessment_snapshot,
            rag_context=rag_context_block,
            history_formatted=history_formatted,
            current_message=clean_user_msg,
        )

        try:
            resp = await self.llm.generate_chat_response(
                messages=[{"role": "user", "content": chat_prompt}],
                system_prompt=CHAT_SYSTEM_PROMPT,
                temperature=settings.AI_TEMPERATURE,
            )
            raw_reply = resp.text
        except Exception as exc:
            logger.error("Chat LLM invocation failed: %s. Using safe fallback reply.", str(exc))
            raw_reply = (
                "Healix is temporarily experiencing communication delays with the AI service. "
                "If you have concerning or worsening symptoms, please consult a healthcare professional."
            )

        # Apply safety validations to chat output
        safe_reply = ClinicalSafetyValidator.sanitize_diagnostic_certainty(raw_reply)
        safe_reply = ClinicalSafetyValidator.validate_prescriptions(safe_reply)

        # Guarantee educational reminder
        if "medical diagnosis" not in safe_reply.lower() and "healix" not in safe_reply.lower():
            safe_reply += "\n\n*Healix provides health information and triage support, not a medical diagnosis.*"

        latency = (time.perf_counter() - start) * 1000
        ai_tracker.record(
            operation_type="chat_interaction",
            latency_ms=latency,
            retrieval_count=len(retrieved_chunks),
            validation_status="SUCCESS",
        )

        return safe_reply

    def _build_emergency_fallback_response(
        self,
        description: str,
        symptoms: List[Dict[str, Any]],
        triage_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Emergency safe response prioritizing life-safety over LLM speculation."""
        return {
            "summary": (
                "CRITICAL MEDICAL ALERT: Reported symptoms triggered high-priority emergency safety rules. "
                + triage_result.get("message", "Immediate emergency evaluation is strongly advised.")
            ),
            "urgency_level": UrgencyLevel.EMERGENCY.value,
            "possible_explanations": [
                {
                    "title": "Acute Medical Emergency Evaluation Required",
                    "description": "Symptoms reported require immediate in-person diagnostic evaluation (such as ECG, imaging, or laboratory tests) to rule out life-threatening acute cardiovascular, respiratory, or neurological conditions.",
                    "match_level": "Immediate Clinical Concern",
                    "supporting_information": ["Triggered deterministic emergency safety indicators"],
                }
            ],
            "general_guidance": [
                "Call 911 or local emergency services immediately.",
                "Do not drive yourself to the emergency department if experiencing chest pain, severe shortness of breath, or weakness.",
                "Notify someone nearby about your symptoms.",
            ],
            "warning_signs": [
                "Chest pressure radiating to the arm or jaw",
                "Severe difficulty breathing or gasping",
                "Sudden weakness, facial drooping, or slurred speech",
                "Thunderclap explosive headache",
            ],
            "sources": [
                {
                    "title": "Adult Emergency Symptoms and Immediate Actions",
                    "organization": "Centers for Disease Control and Prevention (CDC)",
                    "url": "https://www.cdc.gov/heart-disease/signs-symptoms/index.html",
                    "relevance": 1.0,
                },
                {
                    "title": "WHO Emergency Clinical Guidelines",
                    "organization": "World Health Organization (WHO)",
                    "url": "https://www.who.int",
                    "relevance": 1.0,
                },
            ],
            "disclaimer": STANDARD_MEDICAL_DISCLAIMER,
        }

    def _build_safe_fallback_analysis(
        self, symptoms: List[Dict[str, Any]], urgency: str
    ) -> SymptomAnalysisResponse:
        """Deterministic fallback analysis when LLM service is temporarily offline."""
        names = [s.get("name", "") for s in symptoms]
        return SymptomAnalysisResponse(
            symptoms=names,
            duration=["recent"],
            severity=["moderate"],
            possible_explanations=[
                PossibleExplanationItem(
                    title="Physiological Functional Discomfort",
                    description="Symptoms may be consistent with transient functional or viral etiologies. Clinical in-person evaluation is recommended if discomfort persists.",
                    supporting_information=["Baseline clinical evaluation rules"],
                    match_level="Possible Consideration",
                )
            ],
            follow_up_questions=["Has your symptom pattern changed over the past 24 hours?"],
            warning_signs=[
                "Sudden severe pain",
                "Shortness of breath or chest tightness",
                "High persistent fever with stiff neck",
            ],
            general_guidance=[
                "Ensure quiet rest and drink adequate fluids.",
                "Seek medical attention if symptoms intensify.",
            ],
            uncertainties=["Clinical evaluation is required for accurate determination."],
        )

    def _default_authoritative_sources(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Evidence-Based Clinical Guidelines",
                "organization": "Mayo Clinic",
                "url": "https://www.mayoclinic.org",
                "relevance": 0.9,
            },
            {
                "title": "Global Primary Healthcare Standards",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int",
                "relevance": 0.88,
            },
        ]
