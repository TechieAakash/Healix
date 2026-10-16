from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from app.models.conversation import Conversation
from app.models.message import Message


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_and_user(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all_by_user(self, user_id: str, skip: int = 0, limit: int = 20) -> List[Conversation]:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_by_user(self, user_id: str) -> int:
        stmt = select(func.count(Conversation.id)).where(Conversation.user_id == user_id)
        return self.db.execute(stmt).scalar() or 0

    def create(self, conversation: Conversation) -> Conversation:
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def add_message(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def delete(self, conversation: Conversation) -> None:
        self.db.delete(conversation)
        self.db.commit()
