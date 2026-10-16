from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class MessageCreateRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    message_id: str = Field(validation_alias="id")
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ConversationCreateRequest(BaseModel):
    title: Optional[str] = "Health Inquiry"


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)
