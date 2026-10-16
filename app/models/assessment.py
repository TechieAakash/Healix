import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.constants import AssessmentStatus, UrgencyLevel
from app.models.symptom import assessment_symptoms


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default=AssessmentStatus.STARTED.value,
        nullable=False,
    )
    urgency_level: Mapped[str] = mapped_column(
        String(50),
        default=UrgencyLevel.UNKNOWN.value,
        nullable=False,
    )
    user_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="assessments")
    symptoms: Mapped[List["Symptom"]] = relationship(
        "Symptom", secondary=assessment_symptoms, back_populates="assessments"
    )
    follow_up_questions: Mapped[List["FollowUpQuestion"]] = relationship(
        "FollowUpQuestion", back_populates="assessment", cascade="all, delete-orphan", order_by="FollowUpQuestion.order_index"
    )
    report: Mapped[Optional["Report"]] = relationship(
        "Report", back_populates="assessment", cascade="all, delete-orphan", uselist=False
    )
