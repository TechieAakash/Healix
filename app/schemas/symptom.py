from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SymptomCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    severity: int = Field(default=5, ge=1, le=10, description="Symptom severity scale from 1 to 10")
    body_location: Optional[str] = Field(None, max_length=100)
    duration: Optional[str] = Field(None, max_length=100)
    frequency: Optional[str] = Field(None, max_length=100)


class SymptomUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    severity: Optional[int] = Field(None, ge=1, le=10)
    body_location: Optional[str] = None
    duration: Optional[str] = None
    frequency: Optional[str] = None


class SymptomResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    severity: int
    body_location: Optional[str] = None
    duration: Optional[str] = None
    frequency: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
