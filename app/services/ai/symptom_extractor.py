"""
Symptom Extraction and Normalization Service.
Translates unstructured clinical natural language into structured symptom entities,
normalizes colloquial expressions against standard clinical concepts,
and preserves the original text for full auditability.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from app.services.ai.llm.base import BaseLLMProvider
from app.services.ai.llm.provider import get_llm_provider
from app.services.ai.schemas import (
    SymptomExtractionResponse,
    ExtractedSymptomItem,
)
from app.services.ai.prompts.symptom_extraction import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT_TEMPLATE,
)

logger = logging.getLogger("healix.ai.symptom_extractor")

# Clinical normalization dictionary for colloquial variations
NORMALIZATION_MAP: Dict[str, str] = {
    "head pain": "headache",
    "pain in my head": "headache",
    "pain in head": "headache",
    "my head hurts": "headache",
    "head hurts": "headache",
    "throbbing head": "headache",
    "head pounding": "headache",
    "cephalalgia": "headache",

    "stomach ache": "abdominal pain",
    "stomach pain": "abdominal pain",
    "belly ache": "abdominal pain",
    "belly pain": "abdominal pain",
    "tummy ache": "abdominal pain",
    "tummy pain": "abdominal pain",
    "gut pain": "abdominal pain",
    "abdominal cramps": "abdominal pain",

    "short of breath": "shortness of breath",
    "shortness of breath": "shortness of breath",
    "trouble breathing": "shortness of breath",
    "difficulty breathing": "shortness of breath",
    "can't catch breath": "shortness of breath",
    "cannot breathe": "shortness of breath",
    "breathless": "shortness of breath",
    "winded": "shortness of breath",

    "chest tightness": "chest discomfort",
    "chest pain": "chest discomfort",
    "pressure on chest": "chest discomfort",
    "tight chest": "chest discomfort",
    "chest ache": "chest discomfort",

    "throwing up": "nausea / vomiting",
    "vomited": "nausea / vomiting",
    "puking": "nausea / vomiting",
    "nauseous": "nausea",
    "queasy": "nausea",
    "sick to my stomach": "nausea",

    "running a fever": "fever",
    "feverish": "fever",
    "high temp": "fever",
    "high temperature": "fever",

    "lightheaded": "dizziness",
    "lightheadedness": "dizziness",
    "room spinning": "vertigo / dizziness",
    "woozy": "dizziness",

    "sore throat": "sore throat",
    "throat hurts": "sore throat",
    "scratchy throat": "sore throat",
    "pain swallowing": "odynophagia / throat pain",

    "tired": "fatigue",
    "exhausted": "fatigue",
    "lethargic": "fatigue",
    "low energy": "fatigue",
}


class SymptomExtractor:
    """
    Extracts structured symptoms from patient text and applies ontology normalization.
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_llm_provider()

    @staticmethod
    def normalize_term(term: str) -> str:
        """Normalizes a raw symptom term or expression."""
        clean = term.strip().lower()
        if clean in NORMALIZATION_MAP:
            return NORMALIZATION_MAP[clean]
        for pattern, normalized in NORMALIZATION_MAP.items():
            if pattern in clean:
                return normalized
        return clean

    async def extract_and_normalize(self, text: str) -> Dict[str, Any]:
        """
        Main extraction entry point.
        Extracts structured entities, normalizes terms, and preserves original text.
        """
        if not text or not text.strip():
            return {
                "original_text": text,
                "normalized_symptoms": [],
                "associated_features": [],
                "raw_input_summary": "Empty input provided.",
            }

        prompt = EXTRACTION_USER_PROMPT_TEMPLATE.format(user_input=text.strip())

        try:
            extraction_res: SymptomExtractionResponse = await self.llm.generate_structured(
                schema=SymptomExtractionResponse,
                prompt=prompt,
                system_prompt=EXTRACTION_SYSTEM_PROMPT,
                temperature=0.1,
            )
        except Exception as e:
            logger.warning("LLM symptom extraction failed (%s). Falling back to rule-based extractor.", str(e))
            extraction_res = self._fallback_rule_based_extractor(text)

        # Normalize extracted symptom names while recording original identifiers
        normalized_symptoms = []
        for s in extraction_res.symptoms:
            norm_name = self.normalize_term(s.name)
            normalized_symptoms.append({
                "original_name": s.name,
                "normalized_name": norm_name,
                "name": norm_name,
                "location": s.location or "unspecified",
                "severity": s.severity or "unknown",
                "duration": s.duration or "unknown",
                "extraction_type": s.extraction_type or "explicit",
            })

        return {
            "original_text": text,
            "normalized_symptoms": normalized_symptoms,
            "associated_features": extraction_res.associated_features,
            "raw_input_summary": extraction_res.raw_input_summary or f"Extracted {len(normalized_symptoms)} symptoms from input.",
        }

    def _fallback_rule_based_extractor(self, text: str) -> SymptomExtractionResponse:
        """Deterministic regex-based fallback extractor for zero-downtime resiliency."""
        lower = text.lower()
        symptoms = []
        associated = []

        if "head" in lower:
            loc = "right side" if "right" in lower else ("left side" if "left" in lower else "bilateral")
            dur = "1 day" if "yesterday" in lower or "1 day" in lower else "unspecified"
            symptoms.append(ExtractedSymptomItem(
                name="headache",
                location=loc,
                severity="moderate",
                duration=dur,
                extraction_type="inferred" if "headache" not in lower else "explicit",
            ))
        if "nausea" in lower or "nauseous" in lower or "sick" in lower:
            symptoms.append(ExtractedSymptomItem(
                name="nausea",
                location="systemic",
                severity="mild",
                duration="unspecified",
                extraction_type="explicit",
            ))
        if "light" in lower or "photophobia" in lower:
            associated.append("photophobia / light sensitivity")
        if "chest" in lower:
            symptoms.append(ExtractedSymptomItem(
                name="chest discomfort",
                location="retrosternal",
                severity="moderate",
                duration="unspecified",
                extraction_type="explicit",
            ))
        if "fever" in lower or "hot" in lower:
            symptoms.append(ExtractedSymptomItem(
                name="fever",
                location="systemic",
                severity="moderate",
                duration="unspecified",
                extraction_type="explicit",
            ))

        if not symptoms:
            symptoms.append(ExtractedSymptomItem(
                name="unspecified health concern",
                location="unspecified",
                severity="unknown",
                duration="unknown",
                extraction_type="unknown",
            ))

        return SymptomExtractionResponse(
            symptoms=symptoms,
            associated_features=associated,
            raw_input_summary="Fallback rule-based extraction performed.",
        )
