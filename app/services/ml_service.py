from abc import ABC, abstractmethod
from typing import List, Dict, Any


class MLService(ABC):
    """
    Abstract interface for Phase 2 Machine Learning models.
    Supports preliminary feature classification and risk scoring.
    Note: Output is an informational heuristic and never a clinical diagnosis.
    """

    @abstractmethod
    async def predict_symptom_category(self, symptom_text: str) -> str:
        """Classify natural language symptom into an anatomical or physiological domain."""
        pass

    @abstractmethod
    async def estimate_risk_score(self, symptoms: List[Dict[str, Any]]) -> float:
        """Calculates a normalized heuristic score (0.0 to 1.0) indicating urgency."""
        pass


class MockMLService(MLService):
    """Placeholder ML service for Phase 1 testing."""

    async def predict_symptom_category(self, symptom_text: str) -> str:
        text = symptom_text.lower()
        if "head" in text:
            return "Neurological / Cranial"
        if "chest" in text or "breath" in text:
            return "Cardiopulmonary"
        if "stomach" in text or "nausea" in text:
            return "Gastrointestinal"
        return "General / Systemic"

    async def estimate_risk_score(self, symptoms: List[Dict[str, Any]]) -> float:
        if not symptoms:
            return 0.1
        severities = [s.get("severity", 5) for s in symptoms]
        avg = sum(severities) / len(severities)
        return round(avg / 10.0, 2)
