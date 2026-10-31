from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr, Field

# --- Auth Schemas ---
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    date_of_birth: Optional[str] = None
    biological_sex: Optional[str] = None
    clinical_consent_acknowledged: bool = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400

class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    date_of_birth: Optional[str]
    biological_sex: Optional[str]
    created_at: str

# --- Assessment Schemas ---
class ParseSymptomsRequest(BaseModel):
    free_text: str

class ParseSymptomsResponse(BaseModel):
    extracted_symptom_ids: List[str]
    extracted_location_ids: List[str]
    duration: Optional[str] = None
    severity: Optional[str] = None
    character: Optional[str] = None
    negated_facts: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    source: str = "DETERMINISTIC"

class StartAssessmentRequest(BaseModel):
    primary_complaint: str
    symptom_ids: List[str] = Field(default_factory=list)
    location_ids: List[str] = Field(default_factory=list)
    duration: Optional[str] = None
    severity: Optional[str] = "Moderate"
    character: Optional[str] = None

class SubmitAdaptiveAnswerRequest(BaseModel):
    question_id: str
    fact_name: str
    value: str  # "TRUE" | "FALSE" | "UNKNOWN" | "NOT_APPLICABLE" | categorical string
    raw_response: Optional[Any] = None

class QuestionOptionSchema(BaseModel):
    id: str
    label: str
    fact_value: str
    is_red_flag: bool = False

class AdaptiveQuestionResponse(BaseModel):
    has_more_questions: bool
    question: Optional[Dict[str, Any]] = None
    answered_count: int = 0
    emergency_detected: bool = False
    emergency_message: Optional[str] = None

class FactInput(BaseModel):
    fact_name: str
    value: str  # "TRUE" | "FALSE" | "UNKNOWN" | "NOT_APPLICABLE"
    raw_response: Optional[Any] = None

class CreateAssessmentRequest(BaseModel):
    primary_complaint: str
    symptom_onset_date: Optional[str] = None

class EvaluateAssessmentRequest(BaseModel):
    answers: List[FactInput]

class ConclusionItem(BaseModel):
    id: str
    rule_id: str
    category: str
    summary: str
    detailed_explanation: str
    recommendation_tier: str
    confidence: float
    actionable_steps: List[str] = Field(default_factory=list)

class AssessmentResponse(BaseModel):
    assessment_id: str
    user_id: str
    kb_version: str
    status: str
    emergency_flagged: bool
    primary_complaint: str
    conclusions: List[ConclusionItem]
    created_at: str

class AssessmentSummaryItem(BaseModel):
    id: str
    primary_complaint: str
    status: str
    emergency_flagged: bool
    top_conclusion: Optional[str]
    created_at: str

# --- Observation & Timeline Schemas ---
class CreateObservationRequest(BaseModel):
    title: str
    notes: Optional[str] = None
    severity: str = "MILD"
    assessment_id: Optional[str] = None

class ObservationResponse(BaseModel):
    id: str
    user_id: str
    assessment_id: Optional[str]
    title: str
    notes: Optional[str]
    severity: str
    recorded_at: str

# --- Report Schemas ---
class ReportResponse(BaseModel):
    id: str
    assessment_id: str
    title: str
    checksum_sha256: str
    created_at: str
    report_data: Dict[str, Any]

# --- AI Lab Schemas ---
class SearchRequest(BaseModel):
    algorithm: str = "A_STAR"  # "A_STAR" | "HILL_CLIMBING" | "SIMULATED_ANNEALING"
    start_node: str = "Triage"
    goal_node: str = "Specialist_Neurology"

class UnificationRequest(BaseModel):
    term1: str = "AllergicTo(?patient, Penicillin)"
    term2: str = "AllergicTo(John_Doe, ?drug)"

class ResolutionRequest(BaseModel):
    clauses: List[List[str]] = [
        ["P", "Q"],
        ["~P", "Q"],
        ["P", "~Q"],
        ["~P", "~Q"]
    ]

class BayesRequest(BaseModel):
    query_variable: str = "Flu"
    evidence: Dict[str, bool] = {"Fever": True, "Fatigue": True}

class FuzzyRequest(BaseModel):
    temperature_celsius: float = 38.6

