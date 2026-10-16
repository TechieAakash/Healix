from typing import List, Dict, Any, Optional
from app.utils.constants import UrgencyLevel

RED_FLAG_RULES = [
    {
        "id": "RULE_CARDIO_001",
        "category": "cardiovascular",
        "keywords": ["chest pain", "chest pressure", "radiating to arm", "radiating to jaw"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Potential acute coronary or cardiopulmonary warning signs detected.",
    },
    {
        "id": "RULE_RESP_001",
        "category": "respiratory",
        "keywords": ["shortness of breath at rest", "cannot breathe", "stridor", "blue lips", "gasping"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Severe respiratory distress warning signs detected.",
    },
    {
        "id": "RULE_NEURO_001",
        "category": "neurological",
        "keywords": ["facial drooping", "slurred speech", "sudden arm weakness", "sudden loss of vision", "thunderclap headache", "worst headache of my life"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Acute neurological emergency signs detected (e.g. stroke or intracranial hemorrhage alert).",
    },
    {
        "id": "RULE_HEM_001",
        "category": "hemorrhage",
        "keywords": ["coughing up blood", "uncontrolled bleeding", "vomiting blood", "black tarry stools"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Signs of significant hemorrhage or gastrointestinal bleeding.",
    },
    {
        "id": "RULE_SEV_001",
        "category": "severity_threshold",
        "severity_min": 9,
        "urgency": UrgencyLevel.URGENT.value,
        "description": "Extreme self-reported symptom severity (>= 9/10).",
    },
    {
        "id": "RULE_ABDO_001",
        "category": "gastrointestinal",
        "keywords": ["severe abdominal pain", "rigid abdomen", "rebound tenderness"],
        "urgency": UrgencyLevel.URGENT.value,
        "description": "Potential acute peritoneal irritation requiring same-day clinical palpation.",
    },
]


class TriageService:
    """
    Deterministic Safety-First Triage Engine.
    Independent from LLMs to prevent AI hallucinations in emergency situations.
    """

    def __init__(self, rules: Optional[List[Dict[str, Any]]] = None):
        self.rules = rules or RED_FLAG_RULES

    def evaluate(self, description: str = "", symptoms: List[Dict[str, Any]] = None, answers: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        symptoms = symptoms or []
        answers = answers or []

        # Combine all textual context
        text_corpus = (
            f"{description} "
            + " ".join([f"{s.get('name', '')} {s.get('description', '')}" for s in symptoms])
            + " ".join([f"{a.get('answer', '')}" for a in answers])
        ).lower()

        triggered_rules = []
        highest_urgency = UrgencyLevel.ROUTINE.value

        for rule in self.rules:
            # Keyword matching check
            if "keywords" in rule:
                for kw in rule["keywords"]:
                    if kw.lower() in text_corpus:
                        triggered_rules.append(rule)
                        if rule["urgency"] == UrgencyLevel.EMERGENCY.value:
                            highest_urgency = UrgencyLevel.EMERGENCY.value
                        elif rule["urgency"] == UrgencyLevel.URGENT.value and highest_urgency != UrgencyLevel.EMERGENCY.value:
                            highest_urgency = UrgencyLevel.URGENT.value
                        break

            # Severity threshold check
            if "severity_min" in rule:
                for s in symptoms:
                    if s.get("severity", 0) >= rule["severity_min"]:
                        triggered_rules.append(rule)
                        if highest_urgency != UrgencyLevel.EMERGENCY.value:
                            highest_urgency = UrgencyLevel.URGENT.value
                        break

        # Triage summary output
        if highest_urgency == UrgencyLevel.EMERGENCY.value:
            message = (
                "IMPORTANT: Symptoms reported may indicate an acute medical emergency. "
                "Healix cannot determine the cause of your symptoms. "
                "Please contact emergency services (e.g. 911 / 112) or go to the nearest emergency room immediately."
            )
            requires_professional_attention = True
        elif highest_urgency == UrgencyLevel.URGENT.value:
            message = (
                "Symptoms reported suggest you should be evaluated promptly by a healthcare professional "
                "or at an urgent care clinic within 12 to 24 hours."
            )
            requires_professional_attention = True
        else:
            message = (
                "Symptoms reported appear consistent with non-emergent routine conditions. "
                "Schedule a routine appointment with your primary care doctor if symptoms persist or worsen."
            )
            requires_professional_attention = False

        return {
            "urgency_level": highest_urgency,
            "triggered_rules": [r["id"] for r in triggered_rules],
            "message": message,
            "requires_professional_attention": requires_professional_attention,
            "clinical_notes": [r["description"] for r in triggered_rules],
        }
