"""
Deterministic Symptom Extraction and Classification Engine.
Pure Python domain service that parses clinical symptoms, detects negation/hypotheticals,
assigns ontological categories, and flags ambiguous inputs without relying on an LLM.
"""

import re
from typing import List, Dict, Any, Optional
from app.services.clinical.text_normalizer import clean_clinical_text
from app.services.clinical.negation_detector import negation_detector
from app.services.clinical.symptom_registry import SYMPTOM_CONCEPTS, ALIAS_TO_CONCEPT

# Severity keyword patterns
SEVERITY_PATTERNS = [
    (r"\b(?:severe|excruciating|unbearable|intense|terrible|agonizing|worst)\b", 8, "severe"),
    (r"\b(?:moderate|significant|considerable)\b", 5, "moderate"),
    (r"\b(?:mild|slight|minor|a little|faint)\b", 3, "mild"),
    (r"\b(?:severity|scale|rate|rating|pain)?\s*([1-9]|10)\s*(?:/|out of)\s*10\b", None, "numeric"),
    (r"\b([1-9]|10)\s*(?:/|out of)\s*10\b", None, "numeric"),
]

# Duration keyword patterns
DURATION_PATTERNS = [
    r"\b(?:since\s+(?:yesterday|last\s+night|this\s+morning|last\s+week))\b",
    r"\b(?:\d+\s+(?:hours?|days?|weeks?|months?|hrs?))\b",
    r"\b(?:for\s+the\s+past\s+\d+\s+(?:hours?|days?|weeks?))\b",
    r"\b(?:for\s+(?:a\s+few|several|couple\s+of)\s+(?:hours?|days?|weeks?))\b",
    r"\b(?:sudden(?:ly)?|gradual(?:ly)?|chronic|acute)\b",
]


class SymptomEngine:
    """
    Deterministic clinical symptom extractor and classifier.
    """

    def __init__(self):
        # Sort aliases by word length descending so longer phrases match first (e.g. "shortness of breath" before "breath")
        self.sorted_aliases = sorted(ALIAS_TO_CONCEPT.keys(), key=lambda k: len(k.split()), reverse=True)

    def extract(self, text: str = "", preselected_symptoms: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Extracts structured symptoms from free-form text and combines with any preselected structured items.
        """
        cleaned_text = clean_clinical_text(text)
        clauses = negation_detector.split_into_clauses(cleaned_text) if cleaned_text else []

        extracted: List[Dict[str, Any]] = []
        found_concept_ids = set()

        for clause in clauses:
            # Check for severity inside clause
            clause_severity_score, clause_severity_label = self._extract_severity(clause)
            clause_duration = self._extract_duration(clause)

            for alias in self.sorted_aliases:
                pattern = r"\b" + re.escape(alias) + r"\b"
                match = re.search(pattern, clause, re.IGNORECASE)
                if match:
                    concept = ALIAS_TO_CONCEPT[alias]
                    is_neg = negation_detector.is_negated(alias, clause)
                    is_hypo = negation_detector.is_third_party_or_hypothetical(alias, clause)

                    # Deduplicate within same clause unless negation state changes
                    dedup_key = f"{concept['id']}_{is_neg}"
                    if dedup_key not in found_concept_ids:
                        found_concept_ids.add(dedup_key)
                        extracted.append({
                            "concept_id": concept["id"],
                            "canonical_name": concept["canonical_name"],
                            "name": concept["canonical_name"],
                            "original_phrase": match.group(0),
                            "category": concept["category"],
                            "body_location": concept["default_location"],
                            "severity_score": clause_severity_score or 5,
                            "severity_label": clause_severity_label or "moderate",
                            "duration": clause_duration or "unspecified",
                            "is_negated": is_neg,
                            "is_hypothetical": is_hypo,
                        })

        # Integrate any preselected structured symptoms passed as arguments
        if preselected_symptoms:
            for s in preselected_symptoms:
                s_name = s.get("name", "").strip().lower()
                matched_concept = ALIAS_TO_CONCEPT.get(s_name)
                canonical_name = matched_concept["canonical_name"] if matched_concept else s_name
                category = matched_concept["category"] if matched_concept else "general"
                location = s.get("location") or s.get("body_location") or (matched_concept["default_location"] if matched_concept else "unspecified")

                dedup_key = f"{canonical_name}_False"
                if dedup_key not in found_concept_ids:
                    found_concept_ids.add(dedup_key)
                    extracted.append({
                        "concept_id": matched_concept["id"] if matched_concept else f"CUSTOM_{s_name.upper()}",
                        "canonical_name": canonical_name,
                        "name": canonical_name,
                        "original_phrase": s.get("name", ""),
                        "category": category,
                        "body_location": location,
                        "severity_score": s.get("severity", 5),
                        "severity_label": "severe" if s.get("severity", 5) >= 8 else ("mild" if s.get("severity", 5) <= 3 else "moderate"),
                        "duration": s.get("duration", "unspecified"),
                        "is_negated": False,
                        "is_hypothetical": False,
                    })

        active_symptoms = [s for s in extracted if not s["is_negated"] and not s["is_hypothetical"]]
        negated_symptoms = [s for s in extracted if s["is_negated"]]
        hypothetical_symptoms = [s for s in extracted if s["is_hypothetical"]]

        categories = list(dict.fromkeys([s["category"] for s in active_symptoms]))

        # Flag if user typed meaningful text (> 4 words or > 15 chars) but no clinical symptoms matched
        is_unknown_or_ambiguous = False
        if cleaned_text and len(cleaned_text.strip()) > 3 and not active_symptoms:
            is_unknown_or_ambiguous = True

        return {
            "cleaned_text": cleaned_text,
            "all_extracted": extracted,
            "active_symptoms": active_symptoms,
            "negated_symptoms": negated_symptoms,
            "hypothetical_symptoms": hypothetical_symptoms,
            "categories": categories or (["unknown"] if is_unknown_or_ambiguous else ["routine"]),
            "is_unknown_or_ambiguous": is_unknown_or_ambiguous,
        }

    def _extract_severity(self, clause: str) -> tuple[Optional[int], Optional[str]]:
        for pattern, default_val, label in SEVERITY_PATTERNS:
            match = re.search(pattern, clause, re.IGNORECASE)
            if match:
                if label == "numeric":
                    val = int(match.group(1))
                    if val >= 8:
                        return val, "severe"
                    elif val <= 3:
                        return val, "mild"
                    return val, "moderate"
                return default_val, label
        return None, None

    def _extract_duration(self, clause: str) -> Optional[str]:
        for pattern in DURATION_PATTERNS:
            match = re.search(pattern, clause, re.IGNORECASE)
            if match:
                return match.group(0)
        return None


symptom_engine = SymptomEngine()
