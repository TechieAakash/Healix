from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message
from app.repositories.conversation_repository import ConversationRepository
from app.services.ai_service import AIService, MockAIService, get_ai_service
from app.utils.constants import MessageRole
from app.core.exceptions import EntityNotFoundException


class ChatService:
    def __init__(self, db: Session, ai_service: Optional[AIService] = None):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.ai_service = ai_service or get_ai_service()

    def create_conversation(self, user_id: str, title: Optional[str] = "Health Inquiry") -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        return self.conversation_repo.create(conversation)

    def list_conversations(self, user_id: str, page: int = 1, page_size: int = 20) -> Tuple[List[Conversation], int]:
        skip = (page - 1) * page_size
        items = self.conversation_repo.get_all_by_user(user_id, skip=skip, limit=page_size)
        total = self.conversation_repo.count_by_user(user_id)
        return items, total

    def get_conversation(self, conversation_id: str, user_id: str) -> Conversation:
        conversation = self.conversation_repo.get_by_id_and_user(conversation_id, user_id)
        if not conversation:
            raise EntityNotFoundException("Conversation", conversation_id)
        return conversation

    async def send_message(self, conversation_id: str, user_id: str, user_text: str) -> Message:
        conversation = self.get_conversation(conversation_id, user_id)

        # 1. Save User Message
        user_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER.value,
            content=user_text,
        )
        self.conversation_repo.add_message(user_msg)

        # 2. Gather conversation history
        history = [
            {"role": m.role, "content": m.content}
            for m in conversation.messages[-6:]
        ]

        # 3. Retrieve recent assessment context if available
        assessment_ctx = None
        from app.repositories.assessment_repository import AssessmentRepository
        recent_assessments = AssessmentRepository(self.db).get_all_by_user(user_id, skip=0, limit=1)
        if recent_assessments:
            latest = recent_assessments[0]
            assessment_ctx = {
                "assessment_id": latest.id,
                "urgency_level": latest.urgency_level,
                "summary": latest.summary,
            }

        # 4. Call AI Service (Mock in Phase 1, LLM Orchestrator in Phase 2)
        ai_reply = await self.ai_service.chat(user_text, history, assessment_context=assessment_ctx)

        # 4. Save Assistant Message
        assistant_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT.value,
            content=ai_reply,
        )
        saved_assistant = self.conversation_repo.add_message(assistant_msg)
        return saved_assistant
