import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

# Many-to-many association table between assessments and symptoms
assessment_symptoms = Table(
    "assessment_symptoms",
    Base.metadata,
    Column("assessment_id", String(36), ForeignKey("assessments.id", ondelete="CASCADE"), primary_key=True),
    Column("symptom_id", String(36), ForeignKey("symptoms.id", ondelete="CASCADE"), primary_key=True),
)


class Symptom(Base):
    __tablename__ = "symptoms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[int] = mapped_column(Integer, nullable=False, default=5) # Validated 1-10
    body_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    duration: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    frequency: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="symptoms")
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment", secondary=assessment_symptoms, back_populates="symptoms"
    )
