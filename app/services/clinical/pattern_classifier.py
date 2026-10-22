"""Explainable, non-diagnostic symptom pattern classification.

This module uses the project's symptom ontology as a knowledge base and applies
deterministic category rules. It reports which symptom groups were recognized;
the result is not a diagnosis, disease probability, or substitute for care.
"""

from collections import defaultdict
from typing import Any, Dict, List

from app.services.clinical.symptom_engine import symptom_engine


CATEGORY_RULES = {
    "cardiovascular": {
        "title": "Chest and circulation symptoms",
        "description": "The reported symptoms include chest or circulation-related concerns. This category describes the symptoms reported and does not identify their cause.",
    },
    "respiratory": {
        "title": "Breathing and throat symptoms",
        "description": "The reported symptoms include breathing, cough, or throat concerns. This category describes the symptoms reported and does not identify their cause.",
    },
    "neurological": {
        "title": "Headache and balance symptoms",
        "description": "The reported symptoms include headache, dizziness, or related concerns. This category describes the symptoms reported and does not identify their cause.",
    },
    "gastrointestinal": {
        "title": "Digestive symptoms",
        "description": "The reported symptoms involve digestion or the stomach. This category describes the symptoms reported and does not identify their cause.",
    },
    "systemic_infectious": {
        "title": "General body symptoms",
        "description": "The reported symptoms include general body changes such as fever or fatigue. This category describes the symptoms reported and does not identify their cause.",
    },
    "musculoskeletal": {
        "title": "Muscle and joint symptoms",
        "description": "The reported symptoms involve muscles, joints, or the back. This category describes the symptoms reported and does not identify their cause.",
    },
    "dermatological": {
        "title": "Skin symptoms",
        "description": "The reported symptoms involve the skin. This category describes the symptoms reported and does not identify their cause.",
    },
    "general": {
        "title": "Other reported symptoms",
        "description": "These reported symptoms do not match a more specific category in Healix's current symptom list.",
    },
}


class SymptomPatternClassifier:
    """Group extracted symptom concepts into auditable body-system patterns."""

    def classify(
        self,
        description: str,
        symptoms: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        extracted = symptom_engine.extract(
            text=description,
            preselected_symptoms=symptoms,
        )
        grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for symptom in extracted["active_symptoms"]:
            grouped[symptom.get("category", "general")].append(symptom)

        findings: List[Dict[str, Any]] = []
        for category, members in grouped.items():
            rule = CATEGORY_RULES.get(category, CATEGORY_RULES["general"])
            names = list(dict.fromkeys(
                str(item.get("canonical_name") or item.get("name") or "reported symptom").strip()
                for item in members
            ))
            severity_values = [
                value for item in members
                if isinstance((value := item.get("severity_score")), (int, float))
            ]
            severity_note = ""
            if severity_values:
                highest = max(severity_values)
                severity_note = f" Highest recorded severity in this group: {highest}/10."

            findings.append({
                "title": rule["title"],
                "match_level": f"{len(names)} reported symptom{'s' if len(names) != 1 else ''}",
                "description": f"{rule['description']} Reported: {', '.join(names)}.{severity_note}",
                "relevant_symptoms": names,
                "clinical_note": "Rule basis: recognized symptom concepts grouped by the built-in ontology. This is not a likelihood or diagnosis.",
            })

        return findings


symptom_pattern_classifier = SymptomPatternClassifier()
