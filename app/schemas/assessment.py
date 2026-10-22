from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.symptom import SymptomResponse
from app.schemas.report import ReportResponse


class SymptomIntakeItem(BaseModel):
    """Validated structured symptom details supplied with an assessment."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=2, max_length=100)
    severity: int = Field(default=5, ge=1, le=10)
    body_location: Optional[str] = Field(default=None, max_length=100)
    location: Optional[str] = Field(default=None, max_length=100)
    duration: Optional[str] = Field(default=None, max_length=100)
    frequency: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=2000)


class AssessmentCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: Optional[str] = Field(default=None, max_length=5000)
    # Existing user-owned symptom IDs or symptom names for backwards compatibility.
    symptoms: List[str] = Field(default_factory=list, max_length=30)
    symptom_data: List[SymptomIntakeItem] = Field(default_factory=list, max_length=30)


class AssessmentResponse(BaseModel):
    id: str
    user_id: str
    status: str
    urgency_level: str
    user_description: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    symptoms: List[SymptomResponse] = []
    report: Optional[ReportResponse] = None

    model_config = ConfigDict(from_attributes=True)


class AssessmentInitResponse(BaseModel):
    assessment_id: str
    status: str


class AssessmentAnalyzeResponse(BaseModel):
    assessment_id: str
    urgency_level: str
    summary: str
    possible_explanations: List[Any]
    general_guidance: List[str]
    warning_signs: List[str]
    sources: List[Any]
    reasoning_trace: List[Any] = []
    condition_ranking: List[Any] = []
    disclaimer: str
