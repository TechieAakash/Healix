"""Small goal-based controller for the assessment loop.

Percept -> state update -> action selection. It selects workflow actions only;
the deterministic safety engine remains the sole authority for urgency.
"""

from typing import Any, Dict, Iterable, Optional


class AssessmentAgent:
    ACTION_ASK = "ask"
    ACTION_REPORT = "stop_and_report"
    ACTION_ESCALATE = "escalate_emergency"
    ACTION_ABSTAIN = "abstain"

    def update_state(
        self,
        description: str,
        symptoms: Iterable[Dict[str, Any]],
        answers: Iterable[Dict[str, Any]],
        triage: Dict[str, Any],
        ranking: Dict[str, Any],
        questions_remaining: int,
    ) -> Dict[str, Any]:
        """Collect current observations and distinguish absent from negative."""
        return {
            "percept": {
                "description_present": bool(description.strip()),
                "symptom_count": len(symptoms) if hasattr(symptoms, "__len__") else sum(1 for _ in symptoms),
                "answer_count": len(answers) if hasattr(answers, "__len__") else sum(1 for _ in answers),
            },
            "triage": triage,
            "ranking": ranking,
            "questions_remaining": max(0, questions_remaining),
        }

    def select_action(self, state: Dict[str, Any], has_candidate_question: bool = False) -> str:
        """Choose the next assessment action, with emergency urgency locked."""
        if state["triage"].get("urgency_level") == "EMERGENCY":
            return self.ACTION_ESCALATE
        if has_candidate_question and state["questions_remaining"] > 0:
            return self.ACTION_ASK
        if not state["ranking"].get("abstain", True):
            return self.ACTION_REPORT
        if state["percept"]["description_present"] or state["percept"]["symptom_count"]:
            return self.ACTION_ABSTAIN
        return self.ACTION_REPORT
