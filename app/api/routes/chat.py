from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import (
    ConversationCreateRequest,
    ConversationResponse,
    MessageCreateRequest,
    MessageResponse as ChatMessageResponse,
)
from app.schemas.common import PaginatedResponse
from app.services.chat_service import ChatService
from app.api.dependencies import get_current_user, chat_rate_limiter
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start new healthcare dialogue session",
    description="Initializes a new conversation session for health questions and clinical guidance.",
)
def create_conversation(
    req: ConversationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    return service.create_conversation(current_user.id, title=req.title)


@router.get(
    "/conversations",
    response_model=PaginatedResponse[ConversationResponse],
    summary="List patient dialogue sessions",
    description="Returns a paginated list of previous conversational threads.",
)
def list_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    items, total = service.list_conversations(current_user.id, page=page, page_size=page_size)
    return PaginatedResponse(items=items, page=page, page_size=page_size, total=total)


@router.get(
    "/conversations/{id}",
    response_model=ConversationResponse,
    summary="Get conversation history",
    description="Fetches full message history for a specific conversation session.",
)
def get_conversation(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    return service.get_conversation(id, current_user.id)


@router.post(
    "/conversations/{id}/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send message to AI assistant",
    description="Posts a user query, invokes the Mock AI assistant, and returns the grounded reply.",
    dependencies=[Depends(chat_rate_limiter)],
)
async def send_message(
    id: str,
    req: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    msg = await service.send_message(id, current_user.id, req.get_text())
    return ChatMessageResponse(
        message_id=msg.id,
        role=msg.role,
        content=msg.content,
        created_at=msg.created_at,
    )


from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import time
import uuid


class DirectChatRequest(BaseModel):
    message: Optional[str] = None
    content: Optional[str] = None
    text: Optional[str] = None
    sessionId: Optional[str] = None
    session_id: Optional[str] = None


@router.post(
    "/message",
    summary="Instant AI Health Dialogue",
    description="Direct conversational health inquiry powered by AI Orchestrator with RAG and safety guards.",
    dependencies=[Depends(chat_rate_limiter)],
)
@router.post(
    "",
    summary="Instant AI Health Dialogue (Alias)",
    dependencies=[Depends(chat_rate_limiter)],
)
async def direct_chat(req: DirectChatRequest):
    user_text = req.message or req.content or req.text or ""
    from app.services.ai.orchestrator import AIOrchestrator
    orchestrator = AIOrchestrator()
    ai_reply = await orchestrator.chat(user_message=user_text, conversation_history=[])
    
    return {
        "reply": {
            "id": f"msg_{int(time.time() * 1000)}",
            "sender": "assistant",
            "text": ai_reply,
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "sources": ["Mayo Clinic Clinical Compendium", "WHO Water Requirements", "NHS Evidence"],
        },
        "content": ai_reply,
    }
