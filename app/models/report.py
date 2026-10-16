import uuid
from datetime import datetime, timezone
from typing import Any, List, Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.constants import UrgencyLevel


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assessments.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    urgency_level: Mapped[str] = mapped_column(String(50), default=UrgencyLevel.ROUTINE.value, nullable=False)
    
    # Structured clinical analysis collections
    possible_explanations: Mapped[List[Any]] = mapped_column(JSON, nullable=False, default=list)
    general_guidance: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    warning_signs: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    sources: Mapped[List[Any]] = mapped_column(JSON, nullable=False, default=list)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="report")
