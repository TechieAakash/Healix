import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.constants import QuestionType


class FollowUpQuestion(Base):
    __tablename__ = "follow_up_questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    question_type: Mapped[str] = mapped_column(String(50), default=QuestionType.SINGLE_CHOICE.value, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="follow_up_questions")
    answers: Mapped[List["FollowUpAnswer"]] = relationship(
        "FollowUpAnswer", back_populates="question", cascade="all, delete-orphan"
    )


class FollowUpAnswer(Base):
    __tablename__ = "follow_up_answers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("follow_up_questions.id", ondelete="CASCADE"), index=True, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    question: Mapped["FollowUpQuestion"] = relationship("FollowUpQuestion", back_populates="answers")
