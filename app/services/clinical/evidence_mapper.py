"""Conservative offline mapping between Healix intake and DDXPlus evidence.

Only curated aliases are mapped. Unsupported statements and known negatives are
reported separately; they are never invented as positive evidence.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.services.clinical.negation_detector import negation_detector
from app.services.clinical.symptom_ontology import is_a
from app.services.clinical.text_normalizer import clean_clinical_text


PROJECT_ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_MAP_PATH = PROJECT_ROOT / "data" / "models" / "ddxplus_evidence_map.json"


@lru_cache(maxsize=1)
def evidence_definitions() -> Dict[str, Dict[str, Any]]:
    with EVIDENCE_MAP_PATH.open(encoding="utf-8") as source:
        payload = json.load(source)
    return {item["code"]: item for item in payload["evidence"]}


def _phrase_match(phrase: str, text: str) -> bool:
    return bool(re.search(r"(?<!\w)" + re.escape(phrase.casefold()) + r"(?!\w)", text.casefold()))


def severity_membership(value: Any) -> Dict[int, float]:
    """Map an explicit 0–10 value or severity word to fuzzy DDXPlus E_56 values.

    Word centroids use mild=3, moderate=5, severe=8, extreme=10. Triangular
    memberships span adjacent numeric values; the returned grades are normalized.
    """
    if isinstance(value, (int, float)):
        number = max(0.0, min(10.0, float(value)))
        lower = int(number)
        upper = min(10, lower + 1)
        if lower == upper or number == lower:
            return {lower: 1.0}
        return {lower: round(upper - number, 6), upper: round(number - lower, 6)}
    label = str(value or "").casefold()
    centers = {"mild": 3, "slight": 3, "minor": 3, "moderate": 5, "significant": 6, "severe": 8, "intense": 8, "extreme": 10, "unbearable": 10}
    center = next((number for word, number in centers.items() if re.search(r"\b" + word + r"\b", label)), None)
    if center is None:
        return {}
    radius = 2 if center < 10 else 1
    weights = {score: max(0.0, 1.0 - abs(score - center) / (radius + 1)) for score in range(max(0, center - radius), min(10, center + radius) + 1)}
    total = sum(weights.values())
    return {score: weight / total for score, weight in weights.items() if weight > 0}


def duration_membership(value: Any) -> Dict[str, float]:
    """Describe timing fuzzily without pretending DDXPlus has duration evidence.

    DDXPlus has no general symptom-duration field. These memberships are intake
    context only and are excluded from disease likelihood and urgency rules.
    """
    text = str(value or "").casefold()
    if not text:
        return {}
    if re.search(r"\b(today|hours?|1 day|24 hours?|yesterday|few days|couple of days)\b", text):
        return {"recent": 0.8, "ongoing": 0.2}
    if re.search(r"\b(week|weeks|month|months|long[- ]term|chronic)\b", text):
        return {"ongoing": 0.35, "prolonged": 0.65}
    if re.search(r"\b(days?|since)\b", text):
        return {"recent": 0.35, "ongoing": 0.65}
    return {}


class DDXPlusEvidenceMapper:
    """Map only supported, positive symptom evidence into known DDXPlus tokens."""

    def __init__(self):
        self.definitions = evidence_definitions()

    def map_assessment(
        self,
        description: str = "",
        symptoms: Optional[List[Dict[str, Any]]] = None,
        answers: Optional[List[Dict[str, Any]]] = None,
        age: Optional[int] = None,
        sex: Optional[str] = None,
    ) -> Dict[str, Any]:
        symptoms, answers = symptoms or [], answers or []
        text = clean_clinical_text(description)
        clauses = negation_detector.split_into_clauses(text) if text else []
        positive_tokens: Dict[str, float] = {}
        mapped: Dict[str, Dict[str, Any]] = {}
        negated_codes = set()
        hypothetical_codes = set()
        unmapped: List[str] = []
        detected_contexts = set()
        observed_duration = None

        # The checked-in model was trained with these buckets. Use them only
        # when the user's existing profile provides a supported value.
        if age is not None:
            try:
                age_years = int(age)
                bucket = "AGE_0_5" if age_years < 6 else "AGE_6_17" if age_years < 18 else "AGE_18_39" if age_years < 40 else "AGE_40_64" if age_years < 65 else "AGE_65_PLUS"
                positive_tokens[bucket] = 1.0
            except (TypeError, ValueError):
                pass
        sex_value = str(sex or "").strip().casefold()
        if sex_value in {"m", "male"}:
            positive_tokens["SEX_M"] = 1.0
        elif sex_value in {"f", "female"}:
            positive_tokens["SEX_F"] = 1.0

        # Explicitly supplied symptom chips are treated as asserted unless their
        # matching phrase was explicitly negated in free text.
        for code, definition in self.definitions.items():
            if definition.get("is_antecedent"):
                continue
            aliases = definition.get("aliases", [])
            if code == "E_53":
                aliases = [a for a in aliases if a not in {"pain", "ache", "aching", "hurt", "hurts"}]
                aliases += ["pain", "ache", "aching", "hurt", "hurts"]
            found_positive = False
            found_negated = False
            found_hypothetical = False
            for clause in clauses:
                for alias in aliases:
                    if not _phrase_match(alias, clause):
                        continue
                    if negation_detector.is_negated(alias, clause):
                        found_negated = True
                    elif negation_detector.is_third_party_or_hypothetical(alias, clause):
                        found_hypothetical = True
                    else:
                        found_positive = True
            for symptom in symptoms:
                label = str(symptom.get("name", ""))
                for alias in aliases:
                    # Let a recognized child concept satisfy evidence aliases
                    # expressed at a parent level (for example chest_pressure
                    # is_a chest_pain). Negation in the narrative still wins.
                    ontology_match = is_a(label.replace(" ", "_"), alias.replace(" ", "_"))
                    if _phrase_match(alias, label) or ontology_match:
                        # A direct negative in the description overrides a selected chip.
                        if any(_phrase_match(alias, clause) and negation_detector.is_negated(alias, clause) for clause in clauses):
                            found_negated = True
                        else:
                            found_positive = True

            if found_positive:
                detected_contexts.add(definition["context"])
                if definition["data_type"] == "B":
                    positive_tokens[code] = 1.0
                    mapped[code] = {"code": code, "question": definition["question"], "weight": 1.0}
            elif found_negated:
                negated_codes.add(code)
            elif found_hypothetical:
                hypothetical_codes.add(code)

        # Numeric and linguistic severity only map to the dataset's pain intensity
        # variable when a pain concept is present. No severity-to-diagnosis shortcut.
        pain_present = any(c in positive_tokens for c in ("E_53", "E_14", "E_220", "E_216"))
        severity_inputs: List[Any] = [s.get("severity") for s in symptoms if s.get("severity") is not None]
        severity_inputs += [s.get("severity_label") for s in symptoms if s.get("severity_label")]
        for clause in clauses:
            if pain_present and re.search(r"\b(mild|slight|minor|moderate|significant|severe|intense|extreme|unbearable)\b", clause):
                severity_inputs.append(clause)
        severity_value = severity_inputs[0] if severity_inputs else None
        severity_weights = severity_membership(severity_value)
        for score, weight in severity_weights.items():
            token = f"E_56_@_{score}"
            positive_tokens[token] = weight
            mapped[token] = {"code": token, "base_code": "E_56", "question": self.definitions["E_56"]["question"], "weight": weight}

        # Pain descriptors are emitted only when an explicit phrase maps to the
        # dataset's listed multi-choice value.
        pain_descriptor = self.definitions.get("E_54", {})
        for value_code, terms in pain_descriptor.get("value_aliases", {}).items():
            if any(_phrase_match(term, clause) for term in terms for clause in clauses):
                token = f"E_54_@_{value_code}"
                positive_tokens[token] = 1.0
                mapped[token] = {"code": token, "base_code": "E_54", "question": pain_descriptor["question"], "weight": 1.0, "context": "pain"}

        # Follow-up answers are mapped only when the exact code was attached to
        # an asked question. A negative answer records known absence and is not
        # treated as a positive multinomial feature.
        known_negative = set()
        for answer in answers:
            code = str(answer.get("evidence_code") or "")
            if code not in self.definitions:
                continue
            value = str(answer.get("answer", "")).strip().casefold()
            if re.match(r"^(no|nope|not|none|negative|false)\b", value):
                known_negative.add(code)
                positive_tokens.pop(code, None)
                mapped.pop(code, None)
            elif re.match(r"^(yes|yep|yeah|true|present|i do|i have)\b", value):
                if self.definitions[code]["data_type"] == "B":
                    positive_tokens[code] = 1.0
                    mapped[code] = {"code": code, "question": self.definitions[code]["question"], "weight": 1.0}
            elif code == "E_56":
                for score, weight in severity_membership(answer.get("answer")).items():
                    token = f"E_56_@_{score}"
                    positive_tokens[token] = weight
                    mapped[token] = {"code": token, "base_code": "E_56", "question": self.definitions[code]["question"], "weight": weight}

        durations = [s.get("duration") for s in symptoms if s.get("duration")]
        if not durations:
            duration_match = re.search(r"\b(?:since\s+\w+|for\s+)?(?:a\s+few|few|couple\s+of|\d+)\s+(?:hours?|days?|weeks?|months?)\b", text)
            if duration_match:
                durations = [duration_match.group(0)]
        observed_duration = duration_membership(durations[0]) if durations else {}

        detected_contexts = {
            self.definitions.get(item.get("base_code", item["code"]), {}).get("context")
            for item in mapped.values()
        } - {None}

        if not positive_tokens and text:
            # Explicitly list unmatched user concepts, avoiding fabricated DDX codes.
            matched_aliases = [alias for item in self.definitions.values() for alias in item.get("aliases", []) if _phrase_match(alias, text)]
            if not matched_aliases:
                unmapped = [str(item.get("name", "")) for item in symptoms if item.get("name")]
                if not unmapped:
                    unmapped = [text[:120]]

        return {
            "evidence": positive_tokens,
            "mapped_evidence": list(mapped.values()),
            "negated_codes": sorted(negated_codes | known_negative),
            "hypothetical_codes": sorted(hypothetical_codes),
            "unmapped": unmapped,
            "contexts": sorted(detected_contexts),
            "duration_membership": observed_duration,
            "severity_membership": severity_weights,
            "demographic_features_used": [token for token in positive_tokens if token.startswith(("AGE_", "SEX_"))],
            "duration_used_for_condition_ranking": False,
            "duration_used_for_urgency": False,
        }


evidence_mapper = DDXPlusEvidenceMapper()
