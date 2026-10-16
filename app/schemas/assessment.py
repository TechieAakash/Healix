from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict
from app.schemas.symptom import SymptomResponse
from app.schemas.report import ReportResponse


class AssessmentCreateRequest(BaseModel):
    description: Optional[str] = None
    symptoms: List[str] = [] # List of symptom IDs to attach


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
    disclaimer: str
