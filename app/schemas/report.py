from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, ConfigDict


class ExplanationItem(BaseModel):
    title: str
    description: str
    match_level: Optional[str] = None
    relevant_symptoms: Optional[List[str]] = None
    clinical_note: Optional[str] = None


class SourceItem(BaseModel):
    name: str
    topic: Optional[str] = None
    url: Optional[str] = None
    authority: Optional[str] = None


class ReportResponse(BaseModel):
    id: str
    assessment_id: str
    title: str
    summary: str
    urgency_level: str
    possible_explanations: List[Any]
    general_guidance: List[str]
    warning_signs: List[str]
    sources: List[Any]
    reasoning_trace: List[Dict[str, Any]] = []
    condition_ranking: List[Any] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
