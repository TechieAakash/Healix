from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class FollowUpQuestionItem(BaseModel):
    id: str
    question: str
    type: str
    order_index: int = 0

    model_config = ConfigDict(from_attributes=True)


class FollowUpQuestionsListResponse(BaseModel):
    questions: List[FollowUpQuestionItem]


class FollowUpAnswerRequest(BaseModel):
    question_id: str
    answer: str


class FollowUpAnswerResponse(BaseModel):
    id: str
    question_id: str
    answer: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
