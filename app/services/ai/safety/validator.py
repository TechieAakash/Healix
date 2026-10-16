"""
Clinical Safety Validator.
Enforces hard emergency boundaries, non-diagnostic boundaries, prescription prohibitions,
and medical disclaimers on all AI outputs.
"""

import logging
import re
from typing import Dict, Any, List
from app.utils.constants import STANDARD_MEDICAL_DISCLAIMER, UrgencyLevel
from app.core.exceptions import ValidationException

logger = logging.getLogger("healix.ai.safety_validator")


class ClinicalSafetyValidator:
    """
    Guarantees clinical safety integrity of generated AI outputs.
    Enforces that deterministic red-flag rules ALWAYS take precedence over LLM inferences.
    """

    CERTAINTY_PATTERNS = [
        r"you\s+definitely\s+have",
        r"i\s+diagnose\s+you\s+with",
        r"you\s+have\s+been\s+diagnosed\s+with",
        r"this\s+confirms\s+you\s+have",
        r"you\s+are\s+suffering\s+from",
        r"my\s+diagnosis\s+is",
        r"you\s+have\s+(pneumonia|meningitis|a\s+stroke|a\s+heart\s+attack|cancer)",
    ]

    PRESCRIPTION_PATTERNS = [
        r"stop\s+taking\s+(your\s+)?(medication|pills|prescribed)",
        r"cease\s+your\s+medication",
        r"take\s+\d+\s*(mg|milligrams|tablets|pills)",
        r"increase\s+your\s+dose",
        r"decrease\s+your\s+dose",
        r"start\s+taking\s+antibiotics",
    ]

    PROBABILITY_PATTERNS = [
        r"\b\d{1,2}%\s+chance\s+(that\s+)?you\s+have",
        r"\b\d{1,2}%\s+probability\s+of",
    ]

    @classmethod
    def sanitize_diagnostic_certainty(cls, text: str) -> str:
        """
        Replaces definitive diagnostic assertions with tentative clinical possibilities.
        """
        sanitized = text
        for pat in cls.CERTAINTY_PATTERNS:
            sanitized = re.sub(
                pat,
                "your symptoms may be consistent with",
                sanitized,
                flags=re.IGNORECASE,
            )

        # Remove arbitrary numerical diagnostic probabilities
        for pat in cls.PROBABILITY_PATTERNS:
            sanitized = re.sub(
                pat,
                "clinical consideration regarding",
                sanitized,
                flags=re.IGNORECASE,
            )

        return sanitized

    @classmethod
    def validate_prescriptions(cls, text: str) -> str:
        """
        Blocks and strips prescription instructions or dosage directions.
        """
        sanitized = text
        for pat in cls.PRESCRIPTION_PATTERNS:
            if re.search(pat, sanitized, re.IGNORECASE):
                logger.warning("Dangerous prescription instruction detected and neutralized: %s", pat)
                sanitized = re.sub(
                    pat,
                    "discuss any medication or dosage adjustments exclusively with your prescribing doctor",
                    sanitized,
                    flags=re.IGNORECASE,
                )
        return sanitized

    @classmethod
    def enforce_emergency_boundary(
        cls,
        deterministic_urgency: str,
        ai_response_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        HARD SAFETY BOUNDARY:
        If deterministic triage classified the case as EMERGENCY,
        the LLM CANNOT downgrade the urgency or present a casual reassurance.
        """
        if deterministic_urgency == UrgencyLevel.EMERGENCY.value:
            # Force emergency status
            ai_response_data["urgency_level"] = UrgencyLevel.EMERGENCY.value

            # If the LLM failed to emphasize emergency, prepend urgent warning
            summary = ai_response_data.get("summary", "")
            if "emergency" not in summary.lower() and "immediate" not in summary.lower():
                ai_response_data["summary"] = (
                    "CRITICAL SAFETY NOTICE: Symptoms reported indicate a potential medical emergency. "
                    "Seek immediate emergency medical evaluation (911 / 112) or go to the nearest emergency department. "
                    + summary
                )

            # Ensure warning signs contain emergency red flag
            warning_signs = ai_response_data.get("warning_signs", [])
            if not any("emergency" in w.lower() or "immediate" in w.lower() for w in warning_signs):
                warning_signs.insert(0, "Potential acute emergency signs detected requiring immediate in-person evaluation.")
            ai_response_data["warning_signs"] = warning_signs

        elif deterministic_urgency == UrgencyLevel.URGENT.value:
            # Cannot downgrade from URGENT to ROUTINE
            if ai_response_data.get("urgency_level") == UrgencyLevel.ROUTINE.value:
                ai_response_data["urgency_level"] = UrgencyLevel.URGENT.value

        return ai_response_data

    @classmethod
    def validate_and_sanitize_response(
        cls,
        response_dict: Dict[str, Any],
        deterministic_urgency: str = UrgencyLevel.ROUTINE.value,
    ) -> Dict[str, Any]:
        """
        Full safety inspection pipeline for an AI response dictionary.
        """
        # 1. Sanitize summary text
        summary = response_dict.get("summary", "")
        summary = cls.sanitize_diagnostic_certainty(summary)
        summary = cls.validate_prescriptions(summary)
        response_dict["summary"] = summary

        # 2. Sanitize explanations
        explanations = response_dict.get("possible_explanations", [])
        for exp in explanations:
            if isinstance(exp, dict):
                exp["title"] = cls.sanitize_diagnostic_certainty(exp.get("title", ""))
                exp["description"] = cls.sanitize_diagnostic_certainty(exp.get("description", ""))
                exp["description"] = cls.validate_prescriptions(exp.get("description", ""))

        # 3. Sanitize guidance
        guidance = response_dict.get("general_guidance", [])
        response_dict["general_guidance"] = [
            cls.validate_prescriptions(g) for g in guidance
        ]

        # 4. Enforce hard emergency boundary
        response_dict = cls.enforce_emergency_boundary(deterministic_urgency, response_dict)

        # 5. Always guarantee standard medical disclaimer
        response_dict["disclaimer"] = STANDARD_MEDICAL_DISCLAIMER

        return response_dict
