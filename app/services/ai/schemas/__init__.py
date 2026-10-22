"""
Pydantic Schemas for AI Structured Outputs.
Ensures strict validation across symptom extraction, analysis,
adaptive follow-up questioning, RAG citations, and health summaries.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ExtractedSymptomItem(BaseModel):
    name: str = Field(description="Normalized name of symptom (e.g. headache, fever)")
    location: Optional[str] = Field(default="unspecified", description="Anatomical location if specified")
    severity: Optional[str] = Field(default="unknown", description="Reported severity: mild, moderate, severe, or unknown")
    duration: Optional[str] = Field(default="unknown", description="Reported symptom timeline or duration")
    extraction_type: str = Field(default="explicit", description="explicit, inferred, or unknown")


class SymptomExtractionResponse(BaseModel):
    symptoms: List[ExtractedSymptomItem] = Field(default_factory=list)
    associated_features: List[str] = Field(default_factory=list)
    raw_input_summary: Optional[str] = Field(default=None)


class AIQuestionItem(BaseModel):
    question: str = Field(description="Clear, non-technical, easy to answer follow-up question")
    type: str = Field(default="single_choice", description="Question format: single_choice or free_text")
    reasoning: Optional[str] = Field(default="", description="Clinical rationale for asking this specific question")
    order_index: int = Field(default=0)
    options: Optional[List[str]] = Field(default=None, description="Selectable options if single_choice")


class FollowUpQuestionsResponse(BaseModel):
    questions: List[AIQuestionItem] = Field(default_factory=list)
    total_questions: int = Field(default=0)
    safety_rationale: Optional[str] = Field(default="")

    @field_validator("questions")
    @classmethod
    def enforce_question_limit(cls, v: List[AIQuestionItem]) -> List[AIQuestionItem]:
        # Enforce requirement: 5-7 questions max per assessment
        return v[:7]


class SourceCitation(BaseModel):
    title: str = Field(description="Document title or guideline name")
    organization: str = Field(description="Authoritative source organization, e.g. WHO, Mayo Clinic, CDC")
    url: Optional[str] = Field(default=None, description="Verified URL from knowledge base")
    relevance: Optional[float] = Field(default=0.9, description="Semantic relevance score (0.0 - 1.0)")
    topic: Optional[str] = Field(default=None)


class PossibleExplanationItem(BaseModel):
    title: str = Field(description="Educational clinical explanation title (NOT a diagnosis)")
    description: str = Field(description="Objective clinical background and pathophysiology")
    supporting_information: List[str] = Field(default_factory=list)
    match_level: Optional[str] = Field(default="Possible Consideration")
    sources: List[SourceCitation] = Field(default_factory=list)


class SymptomAnalysisResponse(BaseModel):
    symptoms: List[str] = Field(default_factory=list)
    duration: List[str] = Field(default_factory=list)
    severity: List[str] = Field(default_factory=list)
    possible_explanations: List[PossibleExplanationItem] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)
    warning_signs: List[str] = Field(default_factory=list)
    general_guidance: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)


class HealthSummaryResponse(BaseModel):
    summary: str = Field(description="Comprehensive non-diagnostic health narrative")
    reported_symptoms: List[str] = Field(default_factory=list)
    possible_explanations: List[PossibleExplanationItem] = Field(default_factory=list)
    general_guidance: List[str] = Field(default_factory=list)
    warning_signs: List[str] = Field(default_factory=list)
    when_to_seek_care: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    sources: List[SourceCitation] = Field(default_factory=list)


class GroundingCheckResult(BaseModel):
    is_grounded: bool = True
    grounding_score: float = Field(default=1.0, ge=0.0, le=1.0)
    unsupported_claims: List[str] = Field(default_factory=list)
    grounded_claims: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ChatAIResponse(BaseModel):
    message: str
    sources: List[SourceCitation] = Field(default_factory=list)
    warning_signs_flagged: List[str] = Field(default_factory=list)
