import os
import json
import logging
import httpx
from typing import Dict, Any, List, Optional
from ..core.config import settings
from ..clinical_engine.symptoms import SYMPTOM_CATALOGUE, ANATOMICAL_LOCATIONS

logger = logging.getLogger("healix.gemini")

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.model = settings.GEMINI_MODEL
        self.timeout = settings.GEMINI_TIMEOUT_SECONDS

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    async def _call_gemini_generate(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        if not self.is_configured:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1024,
            }
        }
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        content_parts = candidates[0].get("content", {}).get("parts", [])
                        if content_parts:
                            return content_parts[0].get("text", "")
                else:
                    logger.warning(f"Gemini API returned status {res.status_code}: {res.text[:200]}")
        except Exception as e:
            logger.warning(f"Gemini API invocation error: {str(e)}")

        return None

    async def parse_symptom_description(self, free_text: str) -> Dict[str, Any]:
        """
        Extracts recognized symptoms, anatomical locations, duration, severity,
        and explicit negations from free-text using Gemini with deterministic fallback.
        """
        # If Gemini is configured, attempt LLM extraction
        if self.is_configured:
            catalog_summary = [{"id": s.id, "name": s.name, "synonyms": s.synonyms} for s in SYMPTOM_CATALOGUE]
            location_summary = [{"id": l.id, "name": l.name} for l in ANATOMICAL_LOCATIONS]

            system_prompt = (
                "You are an expert clinical NLP parser for the Healix health platform. "
                "Analyze user free-text symptom descriptions and return ONLY valid JSON matching this schema:\n"
                "{\n"
                '  "extracted_symptom_ids": ["sym_headache", ...],\n'
                '  "extracted_location_ids": ["loc_temple_right", ...],\n'
                '  "duration": "< 24 Hours" | "1-3 Days" | "4-7 Days" | "> 1 Month" | null,\n'
                '  "severity": "Mild" | "Moderate" | "Severe" | null,\n'
                '  "character": "Throbbing" | "Sharp" | "Dull" | null,\n'
                '  "negated_facts": ["symptom.fever", ...],\n'
                '  "confidence": 0.0 - 1.0,\n'
                '  "ambiguous_details": ["string", ...]\n'
                "}\n"
                "Strict rule: Only include symptoms and locations present in the provided catalog. "
                "Explicit absence (e.g. 'no fever') must be listed in negated_facts. "
                "If not mentioned, leave it out of negated_facts (never treat unmentioned as negative)."
            )

            prompt = (
                f"Symptom Catalog: {json.dumps(catalog_summary)}\n"
                f"Location Catalog: {json.dumps(location_summary)}\n\n"
                f"User Description: \"{free_text}\"\n\n"
                "Return raw JSON only:"
            )

            raw_response = await self._call_gemini_generate(prompt, system_instruction=system_prompt)
            if raw_response:
                try:
                    cleaned = raw_response.strip()
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                    parsed = json.loads(cleaned.strip())
                    parsed["source"] = "GEMINI_NLP"
                    return parsed
                except Exception as e:
                    logger.warning(f"Failed to parse Gemini JSON: {e}")

        # Deterministic Keyword Fallback
        return self._deterministic_fallback_nlp(free_text)

    def _deterministic_fallback_nlp(self, free_text: str) -> Dict[str, Any]:
        """High-accuracy fallback parser matching keywords and regex patterns."""
        text_lower = free_text.lower()
        extracted_symptoms: List[str] = []
        extracted_locations: List[str] = []
        negated_facts: List[str] = []

        # Check negations first
        if "no fever" in text_lower or "without fever" in text_lower or "haven't had fever" in text_lower:
            negated_facts.append("symptom.fever")
        if "no nausea" in text_lower or "without nausea" in text_lower:
            negated_facts.append("symptom.nausea")
        if "no stiff neck" in text_lower or "no neck stiffness" in text_lower:
            negated_facts.append("symptom.neck_stiffness")
        if "no chest pain" in text_lower:
            negated_facts.append("symptom.chest_pain")

        # Match Symptoms
        for sym in SYMPTOM_CATALOGUE:
            if sym.name.lower() in text_lower:
                extracted_symptoms.append(sym.id)
                continue
            for syn in sym.synonyms:
                if syn.lower() in text_lower:
                    extracted_symptoms.append(sym.id)
                    break

        # Remove negated symptoms from positive extractions
        if "symptom.fever" in negated_facts and "sym_fever" in extracted_symptoms:
            extracted_symptoms.remove("sym_fever")
        if "symptom.nausea" in negated_facts and "sym_nausea" in extracted_symptoms:
            extracted_symptoms.remove("sym_nausea")
        if "symptom.chest_pain" in negated_facts and "sym_chest_pain" in extracted_symptoms:
            extracted_symptoms.remove("sym_chest_pain")
        if "symptom.neck_stiffness" in negated_facts and "sym_neck_stiffness" in extracted_symptoms:
            extracted_symptoms.remove("sym_neck_stiffness")

        # Match Locations
        for loc in ANATOMICAL_LOCATIONS:
            if loc.name.lower() in text_lower:
                extracted_locations.append(loc.id)

        # Basic duration inference
        duration = None
        if "yesterday" in text_lower or "today" in text_lower or "hours" in text_lower:
            duration = "< 24 Hours"
        elif "two days" in text_lower or "2 days" in text_lower or "three days" in text_lower or "3 days" in text_lower:
            duration = "1-3 Days"
        elif "week" in text_lower:
            duration = "4-7 Days"
        elif "month" in text_lower:
            duration = "> 1 Month"

        # Severity inference
        severity = "Moderate"
        if "severe" in text_lower or "worst" in text_lower or "excruciating" in text_lower:
            severity = "Severe"
        elif "mild" in text_lower or "slight" in text_lower or "little" in text_lower:
            severity = "Mild"

        # Character inference
        character = None
        if "throbbing" in text_lower or "pulsing" in text_lower or "pounding" in text_lower:
            character = "Pulsating / Throbbing"
        elif "band" in text_lower or "tight" in text_lower or "pressure" in text_lower:
            character = "Pressing / Tight Band"
        elif "sharp" in text_lower or "stabbing" in text_lower:
            character = "Sharp / Stabbing"
        elif "burning" in text_lower:
            character = "Burning"

        return {
            "extracted_symptom_ids": list(set(extracted_symptoms)),
            "extracted_location_ids": list(set(extracted_locations)),
            "duration": duration,
            "severity": severity,
            "character": character,
            "negated_facts": list(set(negated_facts)),
            "confidence": 0.85 if extracted_symptoms else 0.40,
            "ambiguous_details": [],
            "source": "DETERMINISTIC_RULE_FALLBACK"
        }

    async def generate_assessment_narrative(
        self,
        primary_complaint: str,
        reported_symptoms: List[str],
        clinical_conclusions: List[Dict[str, Any]],
        recommendation_tier: str,
        missing_information: List[str]
    ) -> str:
        """
        Uses Gemini to generate a warm, clear, understandable clinical explanation
        from verified backend findings, emphasizing safety and non-diagnostic boundaries.
        """
        if self.is_configured:
            system_prompt = (
                "You are an empathetic, responsible clinical AI communicator for Healix. "
                "Your role is to translate structured backend triage findings into clear, patient-friendly English.\n"
                "STRICT SAFETY CONSTRAINTS:\n"
                "1. NEVER make definitive diagnoses or claims of medical certainty.\n"
                "2. NEVER invent probability percentages, laboratory values, or medication prescriptions.\n"
                "3. Frame findings as 'possible explanations' or 'symptom constellations'.\n"
                "4. Clearly explain the urgency recommendation and reasons without alarmism.\n"
                "5. Remind the user that Healix is an educational decision-support tool."
            )

            prompt = (
                f"Primary Complaint: {primary_complaint}\n"
                f"Reported Symptoms: {', '.join(reported_symptoms)}\n"
                f"Backend Conclusions: {json.dumps(clinical_conclusions)}\n"
                f"Urgency Tier: {recommendation_tier}\n"
                f"Missing Details: {', '.join(missing_information) if missing_information else 'None'}\n\n"
                "Write a polished, 2-3 paragraph patient summary explaining what the findings mean and what next steps are appropriate:"
            )

            res = await self._call_gemini_generate(prompt, system_instruction=system_prompt)
            if res and len(res.strip()) > 50:
                return res.strip()

        # Deterministic Template Fallback
        return self._deterministic_fallback_narrative(
            primary_complaint=primary_complaint,
            clinical_conclusions=clinical_conclusions,
            recommendation_tier=recommendation_tier
        )

    def _deterministic_fallback_narrative(
        self,
        primary_complaint: str,
        clinical_conclusions: List[Dict[str, Any]],
        recommendation_tier: str
    ) -> str:
        """Produces a structured, evidence-backed narrative without external LLM calls."""
        top_summary = clinical_conclusions[0].get("summary", "Clinical findings identified") if clinical_conclusions else "Assessment completed"
        
        paragraphs = []
        paragraphs.append(
            f"Based on your reported primary concern of \"{primary_complaint}\", the Healix clinical engine evaluated your responses against verified clinical pathways. {top_summary}."
        )

        if recommendation_tier == "EMERGENCY":
            paragraphs.append(
                "CRITICAL ADVICE: Your responses identified warning signs that require immediate emergency evaluation. Please contact local emergency services (112 / 911) or proceed to the nearest emergency department without delay."
            )
        elif recommendation_tier == "URGENT":
            paragraphs.append(
                "Your symptom profile warrants prompt medical attention within the next 24 hours. We recommend contacting an urgent care provider or primary care physician for a formal physical examination."
            )
        elif recommendation_tier == "CONSULT_PHYSICIAN":
            paragraphs.append(
                "While acute emergency indicators were not identified, your symptoms warrant non-emergency consultation with a qualified medical professional. Consider maintaining a symptom diary logging onset times and potential triggers."
            )
        else:
            paragraphs.append(
                "Your reported symptoms are consistent with mild or self-limiting patterns. Supportive home hydration, rest, and routine observation are recommended. Consult a healthcare provider if symptoms worsen or persist."
            )

        paragraphs.append(
            "Note: This assessment is generated for educational decision support and does not constitute a formal diagnosis or prescription."
        )

        return "\n\n".join(paragraphs)
