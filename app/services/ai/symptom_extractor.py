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


from app.services.clinical.symptom_engine import symptom_engine
from app.services.clinical.text_normalizer import clean_clinical_text


class SymptomExtractor:
    """
    Extracts structured symptoms from patient text and applies ontology normalization.
    Prioritizes deterministic Python ontology extraction for reliable safety and zero-downtime offline execution.
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
        Uses deterministic Python symptom engine first, ensuring core triage runs safely without LLM.
        """
        if not text or not text.strip():
            return {
                "original_text": text,
                "normalized_symptoms": [],
                "associated_features": [],
                "raw_input_summary": "Empty input provided.",
            }

        # Step 1: Run deterministic Python symptom engine
        deterministic_result = symptom_engine.extract(text)
        active_symptoms = deterministic_result["active_symptoms"]

        # Check for associated features
        lower = text.lower()
        associated_features = []
        if "bright light" in lower or "photophobia" in lower or "light sensitivity" in lower:
            associated_features.append("photophobia / light sensitivity")
        if "sound" in lower or "phonophobia" in lower:
            associated_features.append("phonophobia / sound sensitivity")

        normalized_symptoms = []
        for s in active_symptoms:
            norm_name = self.normalize_term(s["canonical_name"])
            normalized_symptoms.append({
                "original_name": s.get("original_phrase", s["canonical_name"]),
                "normalized_name": norm_name,
                "name": norm_name,
                "location": s.get("body_location") or "unspecified",
                "severity": s.get("severity_label") or "moderate",
                "duration": s.get("duration") or "unspecified",
                "extraction_type": "explicit",
            })

        # If deterministic extraction found symptoms or LLM is not needed, return immediately
        if normalized_symptoms:
            return {
                "original_text": text,
                "normalized_symptoms": normalized_symptoms,
                "associated_features": associated_features,
                "raw_input_summary": f"Extracted {len(normalized_symptoms)} structured symptoms via deterministic clinical ontology.",
            }

        # Step 2: If deterministic engine didn't match and LLM is available, try LLM as fallback
        try:
            prompt = EXTRACTION_USER_PROMPT_TEMPLATE.format(user_input=text.strip())
            extraction_res: SymptomExtractionResponse = await self.llm.generate_structured(
                schema=SymptomExtractionResponse,
                prompt=prompt,
                system_prompt=EXTRACTION_SYSTEM_PROMPT,
                temperature=0.1,
            )
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
                "associated_features": extraction_res.associated_features or associated_features,
                "raw_input_summary": extraction_res.raw_input_summary or f"Extracted {len(normalized_symptoms)} symptoms from input.",
            }
        except Exception as e:
            logger.info("LLM symptom extraction omitted or failed (%s). Using deterministic output.", str(e))

        return {
            "original_text": text,
            "normalized_symptoms": [],
            "associated_features": associated_features,
            "raw_input_summary": "Unspecified health inquiry or non-specific symptoms.",
        }
