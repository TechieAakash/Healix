import re
from typing import Dict, Any, List
from app.utils.constants import STANDARD_MEDICAL_DISCLAIMER


def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    return True, ""


class AIResponseValidator:
    """
    Validation layer for AI outputs to prevent diagnostic certainty,
    hallucinations, and unsafe medical claims.
    """
    
    CERTAINTY_PHRASES = [
        "you definitely have",
        "you have diagnosed",
        "i diagnose you with",
        "you are suffering from",
        "this confirms you have",
    ]

    @classmethod
    def sanitize_and_validate(cls, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates output from LLM/AI service before returning to client.
        Enforces disclaimer and neutral non-diagnostic terminology.
        """
        summary = response_data.get("summary", "")
        summary_lower = summary.lower()

        # Flag or replace definitive diagnostic claims
        for phrase in cls.CERTAINTY_PHRASES:
            if phrase in summary_lower:
                summary = re.sub(
                    phrase,
                    "your reported symptoms may be consistent with",
                    summary,
                    flags=re.IGNORECASE
                )

        response_data["summary"] = summary

        # Ensure disclaimer is attached
        if "disclaimer" not in response_data or not response_data["disclaimer"]:
            response_data["disclaimer"] = STANDARD_MEDICAL_DISCLAIMER

        return response_data
