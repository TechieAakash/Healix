"""Rule-based and retrieval-grounded provider with no network dependencies."""

import json
import re
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

from app.services.ai.base import BaseLLMProvider, LLMResponse, LLMUsage
from app.services.ai.schemas import (
    AIQuestionItem,
    ChatAIResponse,
    FollowUpQuestionsResponse,
    HealthSummaryResponse,
    PossibleExplanationItem,
    SourceCitation,
    SymptomAnalysisResponse,
    SymptomExtractionResponse,
)
from app.services.ai.safety.validator import ClinicalSafetyValidator
from app.services.clinical.symptom_engine import symptom_engine
from app.services.triage_service import TriageService
from app.utils.constants import STANDARD_MEDICAL_DISCLAIMER, UrgencyLevel

T = TypeVar("T", bound=BaseModel)
_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "do",
    "does", "for", "from", "had", "has", "have", "i", "in", "is", "it", "me",
    "my", "of", "on", "or", "the", "this", "to", "was", "were", "with", "you",
    "your", "what", "when", "where", "how", "why", "can", "could", "should",
}
_SYNONYMS = {
    "tummy": "stomach", "belly": "stomach", "queasy": "nausea",
    "nauseous": "nausea", "woozy": "dizzy", "lightheaded": "dizzy",
    "breathless": "breathing", "winded": "breathing", "pyrexia": "fever",
    "emesis": "vomiting", "loose": "diarrhea", "exhausted": "fatigue",
    "tired": "fatigue", "throbbing": "pain", "aching": "pain",
}


def _section(text: str, start: str, end: Optional[str] = None) -> str:
    start_at = text.find(start)
    if start_at < 0:
        return ""
    start_at += len(start)
    end_at = text.find(end, start_at) if end else -1
    return text[start_at:end_at if end_at >= 0 else None].strip()


def _json_section(text: str, start: str, end: str) -> Any:
    raw = _section(text, start, end)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []


def _tokens(text: str) -> List[str]:
    raw_tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [_SYNONYMS.get(token, token) for token in raw_tokens if token not in _STOPWORDS]


def _prompt_symptoms(prompt: str) -> List[Dict[str, Any]]:
    raw = _json_section(prompt, "Structured Symptoms:\n", "\n\nFollow-up Question Responses:")
    return raw if isinstance(raw, list) else []


def _rag_documents(prompt: str) -> List[Dict[str, Any]]:
    documents = []
    pattern = re.compile(
        r"\[DOCUMENT \d+\]\s*\nSource: (.*?)\s*\nTitle: (.*?)\s*\nTopic: (.*?)\s*\nURL: (.*?)\s*\nEvidence Context: (.*?)\s*\n\[END DOCUMENT \d+\]",
        re.DOTALL,
    )
    for match in pattern.finditer(prompt):
        organization, title, topic, url, body = (part.strip() for part in match.groups())
        documents.append({
            "organization": organization,
            "title": title,
            "topic": topic,
            "url": url,
            "text": body,
        })
    return documents


class LocalLLMProvider(BaseLLMProvider):
    """Deterministic Python provider used by default for offline operation."""

    model_name = "healix-local-rules-v1"

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        reply = self._chat_reply(prompt)
        return self._response(prompt, reply)

    async def generate_structured(
        self,
        schema: Type[T],
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 2,
    ) -> T:
        name = schema.__name__
        if name == "SymptomExtractionResponse":
            raw = _section(prompt, "<<<\n", "\n>>>")
            if not raw:
                raw = _section(prompt, "User Description:\n", "\n\nStructured Symptoms:")
            if not raw:
                raw = _section(prompt, "Patient Description:\n", "\n\nIdentified Symptoms:")
            return self._extract(raw, schema)
        if name == "FollowUpQuestionsResponse":
            return self._follow_ups(prompt, schema)
        if name == "SymptomAnalysisResponse":
            return self._analysis(prompt, schema)
        if name == "HealthSummaryResponse":
            description = _section(prompt, "Patient Description:\n", "\n\nSymptoms:")
            symptoms = _json_section(prompt, "Symptoms:\n", "\n\nFollow-up Answers:")
            answers = _json_section(prompt, "Follow-up Answers:\n", "\n\nTriage Assessment:")
            triage = _section(prompt, "Triage Assessment:\n", "\n\nAnalysis Explanations:")
            explanations = _json_section(prompt, "Analysis Explanations:\n", "\n\nAuthoritative Sources Available:")
            sources = _json_section(prompt, "Authoritative Sources Available:\n", "\n\nGenerate the final health summary")
            names = [s.get("name", "") for s in symptoms if isinstance(s, dict) and s.get("name")]
            summary = self._summary(prompt, SymptomAnalysisResponse(
                symptoms=names,
                possible_explanations=explanations if isinstance(explanations, list) else [],
            ))
            return schema.model_validate({
                "summary": summary,
                "reported_symptoms": names,
                "possible_explanations": explanations if isinstance(explanations, list) else [],
                "general_guidance": self._select_sentences([s.strip() for s in re.split(r"(?<=[.!?])\s+", prompt) if s.strip()], {"guidance", "monitor", "professional"}, 3),
                "warning_signs": [],
                "when_to_seek_care": [triage] if triage else [],
                "limitations": [STANDARD_MEDICAL_DISCLAIMER],
                "sources": sources if isinstance(sources, list) else [],
            })
        if name == "ChatAIResponse":
            return schema.model_validate({"message": self._chat_reply(prompt)})
        try:
            return schema()
        except Exception as exc:
            raise ValueError(f"Local provider does not support schema {name}") from exc

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        prompt = messages[-1].get("content", "") if messages else ""
        reply = self._chat_reply(prompt)
        return self._response(prompt, reply)

    def _response(self, prompt: str, text: str) -> LLMResponse:
        count = max(1, len(_tokens(prompt)))
        return LLMResponse(
            text=text,
            usage=LLMUsage(prompt_tokens=count, completion_tokens=max(1, len(_tokens(text))), total_tokens=count + len(_tokens(text))),
            model=self.model_name,
            finish_reason="stop",
        )

    def _extract(self, text: str, schema: Type[T]) -> T:
        parsed = symptom_engine.extract(text)
        items = []
        location_match = re.search(r"\b(left|right|both)\s+(side|arm|leg|chest|abdomen|lower back|upper back)\b", text, re.IGNORECASE)
        explicit_location = location_match.group(0).lower() if location_match else None
        for item in parsed["active_symptoms"]:
            items.append({
                "name": item["canonical_name"],
                "location": explicit_location or item.get("body_location", "unspecified"),
                "severity": item.get("severity_label", "unknown"),
                "duration": item.get("duration", "unknown"),
                "extraction_type": "explicit",
            })
        associated = []
        lower = text.lower()
        if any(term in lower for term in ("bright light", "light sensitivity", "photophobia")):
            associated.append("light sensitivity")
        if any(term in lower for term in ("sound sensitivity", "sensitive to sound", "phonophobia")):
            associated.append("sound sensitivity")
        return schema.model_validate({
            "symptoms": items,
            "associated_features": associated,
            "raw_input_summary": f"Rule-based ontology extraction recognized {len(items)} symptom concepts.",
        })

    def _follow_ups(self, prompt: str, schema: Type[T]) -> T:
        description = _section(prompt, "Patient Description:\n", "\n\nIdentified Symptoms:")
        raw_symptoms = _json_section(prompt, "Identified Symptoms:\n", "\n\nPrevious Answers (if any):")
        previous = _json_section(prompt, "Previous Answers (if any):\n", "\n\nGenerate focused follow-up questions")
        symptoms = raw_symptoms if isinstance(raw_symptoms, list) else []
        answers = previous if isinstance(previous, list) else []
        parsed = symptom_engine.extract(description, preselected_symptoms=symptoms)
        categories = set(parsed["categories"])
        questions = []
        if "cardiovascular" in categories:
            questions.extend([
                ("Are you having new or severe chest pressure, trouble breathing, or fainting right now?", "Screen for urgent safety concerns."),
                ("When did the chest symptoms begin, and are they getting worse?", "Clarify onset and progression."),
            ])
        if "respiratory" in categories:
            questions.extend([
                ("Are you short of breath while resting or unable to speak comfortably?", "Clarify breathing severity."),
                ("Have you had a fever, and how long have the cough or throat symptoms lasted?", "Clarify related symptoms and duration."),
            ])
        if "neurological" in categories:
            questions.extend([
                ("Did the headache or dizziness begin suddenly, or is it the worst you have experienced?", "Screen for sudden severe onset."),
                ("Have you noticed new weakness, confusion, fainting, or trouble speaking?", "Check for urgent neurological warning signs."),
            ])
        if "gastrointestinal" in categories:
            questions.extend([
                ("Have you been unable to keep fluids down, or noticed blood in vomit or stool?", "Screen for dehydration or bleeding warning signs."),
                ("When did the digestive symptoms begin, and are they worsening?", "Clarify onset and progression."),
            ])
        if not questions:
            questions.extend([
                ("When did these symptoms begin, and have they changed since then?", "Clarify symptom timeline."),
                ("How much are these symptoms affecting your usual daily activities?", "Clarify functional impact."),
            ])
        answered_terms = set(_tokens(" ".join(
            f"{item.get('question', '')} {item.get('answer', '')}" for item in answers if isinstance(item, dict)
        )))
        result = []
        for question, reasoning in questions:
            q_terms = set(_tokens(question))
            # Skip an item when a prior response clearly addresses the same topic.
            key_terms = q_terms.intersection({"when", "begin", "duration", "severity", "worsening", "breathing", "pressure", "fainting", "weakness", "fluids", "blood"})
            if key_terms and len(key_terms.intersection(answered_terms)) >= min(2, len(key_terms)):
                continue
            result.append({"question": question, "type": "free_text", "reasoning": reasoning, "order_index": len(result)})
            if len(result) == 5:
                break
        return schema.model_validate({"questions": result, "total_questions": len(result), "safety_rationale": "Questions are selected by deterministic symptom-category and answer-coverage rules."})

    def _analysis(self, prompt: str, schema: Type[T]) -> T:
        description = _section(prompt, "User Description:\n", "\n\nStructured Symptoms:")
        symptoms = _prompt_symptoms(prompt)
        if not symptoms:
            symptoms = [{"name": s["canonical_name"], "severity": s.get("severity_score")} for s in symptom_engine.extract(description)["active_symptoms"]]
        answers = _json_section(prompt, "Follow-up Question Responses:\n", "\n\nTriage Baseline Status:")
        documents = _rag_documents(prompt)
        triage = _section(prompt, "Triage Baseline Status:\n", "\n\n---")
        if triage == UrgencyLevel.EMERGENCY.value:
            return schema.model_validate({
                "symptoms": [s.get("name", "") for s in symptoms],
                "possible_explanations": [],
                "warning_signs": ["The reported information matched a safety rule requiring emergency attention."],
                "general_guidance": ["Contact local emergency services or seek emergency care now."],
                "uncertainties": ["A remote tool cannot determine the cause of an emergency symptom."],
            })

        explanations = []
        citations = []
        seen = set()
        for doc in documents:
            if not doc["text"] or doc["title"] in seen:
                continue
            seen.add(doc["title"])
            citation = {
                "title": doc["title"],
                "organization": doc["organization"],
                "url": doc["url"] or None,
                "topic": doc["topic"] or None,
                "relevance": 0.8,
            }
            citations.append(citation)
            relevant = [s.get("name", "") for s in symptoms if s.get("name")]
            topic_title = doc["topic"].replace("_", " ").title() if doc["topic"] else "General health"
            explanations.append({
                "title": f"Educational information: {topic_title}",
                "description": self._relevant_excerpt(doc["text"], description, relevant),
                "supporting_information": relevant[:5],
                "match_level": "Related reference material",
                "sources": [citation],
            })
            if len(explanations) == 3:
                break

        content = " ".join(doc["text"] for doc in documents)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", content) if s.strip()]
        guidance = self._select_sentences(sentences, {"guidance", "rest", "hydration", "monitor", "seek", "healthcare", "professional", "avoid", "support"}, 3)
        warnings = self._select_sentences(sentences, {"warning", "emergency", "immediate", "severe", "urgent", "blood", "difficulty", "worsen", "confusion"}, 4)
        if not documents:
            guidance = ["Track when symptoms occur and how they change. Seek professional advice if symptoms persist, worsen, or concern you."]
            warnings = ["Seek urgent help for severe breathing difficulty, new chest pressure, fainting, confusion, sudden weakness, or rapidly worsening symptoms."]
        return schema.model_validate({
            "symptoms": [s.get("name", "") for s in symptoms],
            "duration": list(dict.fromkeys(str(s.get("duration")) for s in symptoms if s.get("duration"))),
            "severity": list(dict.fromkeys(str(s.get("severity")) for s in symptoms if s.get("severity"))),
            "possible_explanations": explanations,
            "follow_up_questions": [],
            "warning_signs": warnings,
            "general_guidance": guidance,
            "uncertainties": [STANDARD_MEDICAL_DISCLAIMER],
        })

    @staticmethod
    def _relevant_excerpt(text: str, description: str, symptoms: List[str]) -> str:
        candidates = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]
        query_terms = set(_tokens(description + " " + " ".join(symptoms)))
        ranked = sorted(
            enumerate(candidates),
            key=lambda pair: (len(query_terms.intersection(_tokens(pair[1]))), -pair[0]),
            reverse=True,
        )
        selected = [sentence for _, sentence in ranked[:2]]
        return " ".join(selected)[:700] if selected else text[:500]

    @staticmethod
    def _select_sentences(sentences: List[str], triggers: set, limit: int) -> List[str]:
        selected = []
        for sentence in sentences:
            lower = sentence.lower()
            if not any(word in lower for word in triggers):
                continue
            if re.search(r"\b\d+\s*(?:mg|mcg|ml|tablets?|pills?)\b|prescrib|dosage|dose of", lower):
                continue
            sanitized = ClinicalSafetyValidator.validate_prescriptions(sentence)
            if sanitized not in selected:
                selected.append(sanitized)
            if len(selected) == limit:
                break
        return selected

    @staticmethod
    def _summary(prompt: str, analysis: SymptomAnalysisResponse) -> str:
        context = _section(prompt, "Triage Assessment:\n", "\n\nAnalysis Explanations:")
        names = ", ".join(analysis.symptoms) or "the symptoms described"
        return f"This offline health information summary covers {names}. {context}. It is educational and does not establish a diagnosis."

    def _chat_reply(self, prompt: str) -> str:
        query = _section(prompt, "CURRENT USER QUERY:\n<<<\n", "\n>>>")
        if not query:
            query = prompt
        clean = query.strip()
        lower = clean.lower()

        medication_request = bool(re.search(
            r"\b(dose|dosage|how many\s+(?:mg|tablets|pills)|how much .*medicine|prescribe|prescription|stop taking|increase .*medication|change .*medication)\b",
            lower,
        ))
        diagnosis_request = bool(re.search(
            r"\b(what (?:disease|illness|condition) do i have|diagnose me|give me (?:a )?diagnosis|do i have [a-z]+)\b",
            lower,
        ))
        if medication_request:
            reply = "I can’t recommend a personal medication dose, prescription, or treatment change. Please ask your prescriber or pharmacist; if you may have taken an unsafe amount, contact local poison control or emergency services."
        elif diagnosis_request:
            reply = "I can’t identify or confirm a disease from a chat. I can explain general health information and help you review warning signs. A qualified clinician can assess your symptoms in context."
        else:
            triage = TriageService().evaluate(clean)
            if triage["urgency_level"] == UrgencyLevel.EMERGENCY.value:
                reply = f"{triage['message']}"
            else:
                documents = _rag_documents(prompt)
                if not documents:
                    reply = "I don’t have a relevant reference passage for that question in the offline knowledge base. Please rephrase it or ask about a supported health topic."
                else:
                    query_terms = set(_tokens(clean))
                    ranked = sorted(
                        documents,
                        key=lambda doc: (
                            len(query_terms.intersection(_tokens(doc["title"]))),
                            len(query_terms.intersection(_tokens(doc["text"]))),
                        ),
                        reverse=True,
                    )
                    selected = ranked[:2]
                    # Multi-topic questions need evidence for each key topic,
                    # not just the first high-overlap document.
                    for term in query_terms:
                        match = next((doc for doc in documents if term in _tokens(doc["title"]) and doc not in selected), None)
                        if match:
                            selected.append(match)
                    parts = []
                    for doc in selected[:3]:
                        excerpt = self._relevant_excerpt(doc["text"], clean, [])
                        source = f"\nSource: [{doc['organization']} — {doc['title']}]({doc['url']})" if doc["url"] else ""
                        parts.append(excerpt + source)
                    reply = "\n\n".join(parts)
            history = _section(prompt, "CONVERSATION HISTORY:\n", "\n\nCURRENT USER QUERY:")
            if re.search(r"\b(my|that|the|latest|last) assessment\b|\breport\b", lower) and "ACTIVE ASSESSMENT CONTEXT" in prompt:
                assessment = _section(prompt, "ACTIVE ASSESSMENT CONTEXT (IF APPLICABLE):\n", "\n\nRETRIEVED CLINICAL KNOWLEDGE:")
                if "Urgency Level:" in assessment and "No active assessment" not in assessment:
                    reply += f"\n\nFrom the assessment context available in this conversation: {assessment.strip()}"
        if "healix provides" not in reply.lower():
            reply += f"\n\n{STANDARD_MEDICAL_DISCLAIMER}"
        return ClinicalSafetyValidator.validate_prescriptions(ClinicalSafetyValidator.sanitize_diagnostic_certainty(reply))
