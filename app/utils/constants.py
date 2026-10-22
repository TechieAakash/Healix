from enum import Enum


class AssessmentStatus(str, Enum):
    STARTED = "STARTED"
    SYMPTOMS_COLLECTED = "SYMPTOMS_COLLECTED"
    FOLLOW_UP = "FOLLOW_UP"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class UrgencyLevel(str, Enum):
    ROUTINE = "ROUTINE"
    URGENT = "URGENT"
    EMERGENCY = "EMERGENCY"
    UNKNOWN = "UNKNOWN"


class MessageRole(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"


class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    SCALE = "scale"
    TEXT = "text"


STANDARD_MEDICAL_DISCLAIMER = (
    "Healix provides health information and triage guidance; it does NOT provide medical diagnosis or treatment. "
    "All summaries are educational considerations to discuss with a licensed physician. "
    "If you experience severe warning signs, contact your local emergency services immediately."
)
