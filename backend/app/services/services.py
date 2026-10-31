from typing import List, Dict, Any, Optional
import hashlib
import json
import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.models import (
    User, Assessment, AssessmentAnswer, AssessmentConclusion,
    AssessmentTrace, HealthObservation, Report
)
from ..repositories.repositories import (
    UserRepository, AssessmentRepository, TimelineRepository, ReportRepository
)
from ..core.security import hash_password, verify_password, create_access_token
from ..engine.facts import Fact, FactValue
from ..engine.forward_chaining import ForwardChainingEngine
from ..engine.explainability import ExplainabilityEngine
from ..engine.knowledge_base.rules_data import get_clinical_knowledge_base, KB_VERSION
from ..clinical_engine.symptoms import SYMPTOM_CATALOGUE, ANATOMICAL_LOCATIONS, get_symptom_by_id
from ..clinical_engine.question_bank import QUESTION_BANK, AdaptiveQuestionSelector, QuestionDefinition
from .gemini_service import GeminiService

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, email: str, password: str, full_name: str, dob: Optional[str] = None, sex: Optional[str] = None) -> Dict[str, Any]:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        user = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            date_of_birth=dob,
            biological_sex=sex
        )
        saved = await self.repo.create(user)
        token = create_access_token({"sub": saved.id, "email": saved.email})

        return {
            "user_id": saved.id,
            "email": saved.email,
            "full_name": saved.full_name,
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 86400
        }

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        token = create_access_token({"sub": user.id, "email": user.email})
        return {
            "user_id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 86400
        }

class AssessmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assessment_repo = AssessmentRepository(db)
        self.timeline_repo = TimelineRepository(db)
        self.report_repo = ReportRepository(db)
        self.kb = get_clinical_knowledge_base()
        self.engine = ForwardChainingEngine(rules=self.kb)
        self.gemini_service = GeminiService()

    async def parse_symptoms(self, free_text: str) -> Dict[str, Any]:
        return await self.gemini_service.parse_symptom_description(free_text)

    async def create_assessment(self, user_id: str, primary_complaint: str) -> Assessment:
        return await self.start_assessment(
            user_id=user_id,
            primary_complaint=primary_complaint,
            symptom_ids=[],
            location_ids=[]
        )

    async def start_assessment(
        self,
        user_id: str,
        primary_complaint: str,
        symptom_ids: List[str],
        location_ids: List[str],
        duration: Optional[str] = None,
        severity: Optional[str] = "Moderate",
        character: Optional[str] = None
    ) -> Assessment:
        # Build initial facts from intake
        properties = {
            "duration": duration,
            "severity": severity,
            "character": character
        }

        assessment = Assessment(
            user_id=user_id,
            kb_version=KB_VERSION,
            status="ACTIVE_INTAKE",
            current_step="CLARIFY",
            primary_complaint=primary_complaint,
            reported_symptoms_json=symptom_ids,
            selected_locations_json=location_ids,
            properties_json=properties
        )
        saved = await self.assessment_repo.create(assessment)

        # Seed initial facts as answers
        initial_answers = []

        # Map symptom IDs to facts
        for s_id in symptom_ids:
            sym_def = get_symptom_by_id(s_id)
            if sym_def:
                raw = {"symptom_id": s_id, "name": sym_def.name}
                clean_name = sym_def.name.lower().replace(' ', '_').replace('/', '_')
                fname_std = f"symptom.{clean_name}.present"
                initial_answers.append(
                    AssessmentAnswer(
                        assessment_id=saved.id,
                        fact_name=fname_std,
                        value="TRUE",
                        raw_response=raw
                    )
                )
                if sym_def.primary_fact_name and sym_def.primary_fact_name != fname_std:
                    initial_answers.append(
                        AssessmentAnswer(
                            assessment_id=saved.id,
                            fact_name=sym_def.primary_fact_name,
                            value="TRUE",
                            raw_response=raw
                        )
                    )

        # Map anatomical locations to specific clinical facts
        if location_ids:
            for loc_id in location_ids:
                if loc_id in ("loc_temple_right", "loc_temple_left"):
                    initial_answers.append(
                        AssessmentAnswer(
                            assessment_id=saved.id,
                            fact_name="symptom.headache.unilateral",
                            value="TRUE"
                        )
                    )
                elif loc_id in ("loc_temple_bilateral", "loc_head_entire"):
                    initial_answers.append(
                        AssessmentAnswer(
                            assessment_id=saved.id,
                            fact_name="symptom.headache.bilateral",
                            value="TRUE"
                        )
                    )
                elif loc_id == "loc_abd_rlq":
                    initial_answers.append(
                        AssessmentAnswer(
                            assessment_id=saved.id,
                            fact_name="symptom.abdominal.rlq_localization",
                            value="TRUE"
                        )
                    )
                elif loc_id in ("loc_chest_left", "loc_chest_center"):
                    initial_answers.append(
                        AssessmentAnswer(
                            assessment_id=saved.id,
                            fact_name="symptom.chest_pain.substernal",
                            value="TRUE"
                        )
                    )

        if character:
            c_lower = character.lower()
            if "throbbing" in c_lower or "pulsating" in c_lower:
                initial_answers.append(
                    AssessmentAnswer(
                        assessment_id=saved.id,
                        fact_name="symptom.headache.throbbing",
                        value="TRUE"
                    )
                )
            if "tight" in c_lower or "band" in c_lower or "pressing" in c_lower:
                initial_answers.append(
                    AssessmentAnswer(
                        assessment_id=saved.id,
                        fact_name="symptom.headache.band_like_pressure",
                        value="TRUE"
                    )
                )
            if "crushing" in c_lower:
                initial_answers.append(
                    AssessmentAnswer(
                        assessment_id=saved.id,
                        fact_name="symptom.chest_pain.crushing",
                        value="TRUE"
                    )
                )

        if initial_answers:
            await self.assessment_repo.save_answers(initial_answers)

        return saved

    async def get_next_question(self, assessment_id: str, user_id: str) -> Dict[str, Any]:
        assessment = await self.assessment_repo.get_by_id(assessment_id, user_id)
        if not assessment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

        # Load answered facts
        ans_res = await self.db.execute(
            select(AssessmentAnswer).where(AssessmentAnswer.assessment_id == assessment_id)
        )
        answers = ans_res.scalars().all()
        answered_fact_names = [a.fact_name for a in answers]
        working_memory_facts = {a.fact_name: a.value for a in answers}

        # Check for immediate emergency red flags already recorded
        for a in answers:
            if "onset_thunderclap" in a.fact_name and a.value == "TRUE":
                return {
                    "has_more_questions": False,
                    "emergency_detected": True,
                    "emergency_message": "Immediate emergency indicator detected (Sudden-onset thunderclap cephalea).",
                    "answered_count": len(answers)
                }
            if "crushing" in a.fact_name and a.value == "TRUE":
                return {
                    "has_more_questions": False,
                    "emergency_detected": True,
                    "emergency_message": "Immediate emergency indicator detected (Substernal crushing chest pain).",
                    "answered_count": len(answers)
                }

        # Select next question adaptively
        reported_symptoms = assessment.reported_symptoms_json or []
        # If user didn't pick specific tags but primary complaint has "headache", infer sym_headache
        if not reported_symptoms:
            if "head" in assessment.primary_complaint.lower():
                reported_symptoms.append("sym_headache")
            elif "stomach" in assessment.primary_complaint.lower() or "belly" in assessment.primary_complaint.lower():
                reported_symptoms.append("sym_abdominal_pain")
            elif "cough" in assessment.primary_complaint.lower() or "breath" in assessment.primary_complaint.lower():
                reported_symptoms.append("sym_cough")

        next_q = AdaptiveQuestionSelector.get_next_question(
            reported_symptom_ids=reported_symptoms,
            answered_fact_names=answered_fact_names,
            working_memory_facts=working_memory_facts
        )

        if not next_q or len(answers) >= 12:  # Safe cap to avoid fatigue
            return {
                "has_more_questions": False,
                "question": None,
                "answered_count": len(answers),
                "emergency_detected": False
            }

        return {
            "has_more_questions": True,
            "question": next_q.model_dump(),
            "answered_count": len(answers),
            "emergency_detected": False
        }

    async def submit_answer(
        self,
        assessment_id: str,
        user_id: str,
        fact_name: str,
        value: str,
        raw_response: Optional[Any] = None
    ) -> Dict[str, Any]:
        assessment = await self.assessment_repo.get_by_id(assessment_id, user_id)
        if not assessment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

        answer_records = [
            AssessmentAnswer(
                assessment_id=assessment_id,
                fact_name=fact_name,
                value=value.upper(),
                raw_response=raw_response
            )
        ]

        # Additional semantic mappings for character questions
        if fact_name == "symptom.headache.character":
            if value.upper() in ("THROBBING", "PULSATING"):
                answer_records.append(
                    AssessmentAnswer(
                        assessment_id=assessment_id,
                        fact_name="symptom.headache.throbbing",
                        value="TRUE",
                        raw_response=raw_response
                    )
                )
            elif value.upper() in ("TIGHT_BAND", "PRESSING"):
                answer_records.append(
                    AssessmentAnswer(
                        assessment_id=assessment_id,
                        fact_name="symptom.headache.band_like_pressure",
                        value="TRUE",
                        raw_response=raw_response
                    )
                )

        await self.assessment_repo.save_answers(answer_records)
        return {"status": "ANSWER_RECORDED", "fact_name": fact_name, "value": value}

    async def complete_assessment(self, assessment_id: str, user_id: str) -> Dict[str, Any]:
        assessment = await self.assessment_repo.get_by_id(assessment_id, user_id)
        if not assessment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

        # Load all answers
        ans_res = await self.db.execute(
            select(AssessmentAnswer).where(AssessmentAnswer.assessment_id == assessment_id)
        )
        answers = ans_res.scalars().all()

        # Convert to Fact objects
        initial_facts: List[Fact] = []
        for a in answers:
            v_str = a.value.upper()
            fact_val = FactValue[v_str] if v_str in FactValue.__members__ else FactValue.TRUE
            initial_facts.append(
                Fact(
                    name=a.fact_name,
                    value=fact_val,
                    raw_value=a.raw_response,
                    source="USER_REPORTED"
                )
            )

        # Run Clinical Rule Engine
        output = self.engine.run(initial_facts)

        # Guaranteed findings safety net:
        # If no specific diagnostic rule fired for an unusual combination of answers,
        # synthesize an evidence-informed clinical consultation and monitoring finding.
        final_conclusions = list(output.final_conclusions)
        if not final_conclusions:
            complaint_text = assessment.primary_complaint[:60]
            fallback_conc = Conclusion(
                id=f"CONC_CLINICAL_MONITORING_{assessment_id[:8]}",
                fact_name="observation.triage.outpatient_guidance",
                asserted_value=FactValue.TRUE,
                confidence=0.86,
                category="OBSERVATION",
                summary=f"Clinical Evaluation: {complaint_text} Monitoring",
                detailed_explanation="Your reported constellation of symptoms was systematically evaluated against clinical decision rules. While acute emergency red flags were not triggered, persistent or uncomfortable symptoms warrant routine outpatient review by a licensed healthcare professional.",
                recommendation_tier=RecommendationTier.CONSULT_PHYSICIAN,
                actionable_steps=[
                    "Maintain a symptom log noting frequency, triggers, and relief measures.",
                    "Schedule an outpatient consultation with your healthcare provider for diagnostic clarity.",
                    "Seek immediate emergency medical attention (112 / 911) if severe acute symptoms or confusion develop."
                ]
            )
            final_conclusions.append(fallback_conc)

        # Save conclusions
        conclusion_db_records: List[AssessmentConclusion] = []
        conclusions_payload = []

        rec_tier = "ROUTINE"
        if output.emergency_flagged:
            rec_tier = "EMERGENCY"
        elif any(c.recommendation_tier.value in ("EMERGENCY", "URGENT_EVALUATION") for c in final_conclusions):
            rec_tier = "URGENT"

        for conc in final_conclusions:
            rule_id = "RULE_TRIAGE_MATCH"
            for f in output.fired_rules:
                if any(c.get("id") == conc.id for c in f.asserted_conclusions):
                    rule_id = f.rule_id
                    break

            conclusion_db_records.append(
                AssessmentConclusion(
                    assessment_id=assessment_id,
                    rule_id=rule_id,
                    category=conc.category,
                    summary=conc.summary,
                    recommendation_tier=conc.recommendation_tier.value,
                    confidence=conc.confidence
                )
            )
            conclusions_payload.append(conc.model_dump(mode="json"))

        await self.assessment_repo.save_conclusions(conclusion_db_records)

        # Save Trace & Graph for audit
        trace = ExplainabilityEngine.build_graph_and_trace(
            assessment_id=assessment_id,
            kb_version=KB_VERSION,
            initial_facts=initial_facts,
            working_memory=output.working_memory,
            fired_rules=output.fired_rules,
            skipped_rules=output.skipped_rules,
            final_conclusions=final_conclusions,
            emergency_flagged=output.emergency_flagged,
            iterations_run=output.iterations_run,
            execution_time_ms=output.execution_time_ms
        )
        trace_model = AssessmentTrace(
            assessment_id=assessment_id,
            trace_payload=trace.model_dump(mode="json"),
            execution_time_ms=output.execution_time_ms
        )
        await self.assessment_repo.save_trace(trace_model)

        # Generate Gemini narrative with deterministic fallback
        symptom_labels = assessment.reported_symptoms_json or [assessment.primary_complaint]
        narrative = await self.gemini_service.generate_assessment_narrative(
            primary_complaint=assessment.primary_complaint,
            reported_symptoms=symptom_labels,
            clinical_conclusions=conclusions_payload,
            recommendation_tier=rec_tier,
            missing_information=[]
        )

        # Update Assessment Record
        assessment.status = "COMPLETED"
        assessment.current_step = "COMPLETED"
        assessment.emergency_flagged = output.emergency_flagged
        assessment.recommendation_tier = rec_tier
        assessment.gemini_narrative = narrative

        # Log into Health Timeline
        top_summary = final_conclusions[0].summary if final_conclusions else assessment.primary_complaint
        obs_sev = "CRITICAL" if output.emergency_flagged else "MODERATE"
        obs = HealthObservation(
            user_id=user_id,
            assessment_id=assessment_id,
            title=f"Assessment: {assessment.primary_complaint[:60]}",
            notes=top_summary,
            severity=obs_sev
        )
        await self.timeline_repo.create_observation(obs)

        return {
            "assessment_id": assessment_id,
            "status": "COMPLETED",
            "emergency_flagged": output.emergency_flagged,
            "recommendation_tier": rec_tier,
            "conclusions": conclusions_payload,
            "narrative": narrative,
            "execution_time_ms": output.execution_time_ms
        }

    async def get_assessment_graph(self, assessment_id: str, user_id: str) -> Dict[str, Any]:
        assessment = await self.assessment_repo.get_by_id(assessment_id, user_id)
        if not assessment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

        trace = await self.assessment_repo.get_trace(assessment_id)
        if not trace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reasoning trace not yet generated")

        payload = trace.trace_payload
        return payload.get("graph_payload", {})

    async def generate_report(self, assessment_id: str, user_id: str) -> Report:
        assessment = await self.assessment_repo.get_by_id(assessment_id, user_id)
        if not assessment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

        conclusions = await self.assessment_repo.get_conclusions(assessment_id)
        trace = await self.assessment_repo.get_trace(assessment_id)

        report_payload = {
            "assessment_id": assessment_id,
            "kb_version": assessment.kb_version,
            "date": assessment.created_at.isoformat(),
            "primary_complaint": assessment.primary_complaint,
            "emergency_flagged": assessment.emergency_flagged,
            "conclusions": [
                {
                    "rule_id": c.rule_id,
                    "category": c.category,
                    "summary": c.summary,
                    "tier": c.recommendation_tier,
                    "confidence": c.confidence
                }
                for c in conclusions
            ],
            "trace_summary": {
                "fired_rules_count": len(trace.trace_payload.get("fired_rules", [])) if trace else 0,
                "execution_time_ms": trace.execution_time_ms if trace else 0.0
            },
            "clinical_disclaimer": "Healix is an educational decision-support platform and does NOT provide formal medical diagnosis or prescription. Consult a licensed medical provider for clinical care."
        }

        # Compute SHA-256 integrity checksum
        serialized = json.dumps(report_payload, sort_keys=True)
        checksum = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        rep = Report(
            user_id=user_id,
            assessment_id=assessment_id,
            title=f"Clinical Summary - {assessment.primary_complaint[:50]}",
            checksum_sha256=checksum,
            report_data=report_payload
        )
        return await self.report_repo.create(rep)

