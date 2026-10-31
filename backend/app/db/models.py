import uuid
import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Float, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from ..core.database import Base

def gen_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    date_of_birth = Column(String(30), nullable=True)
    biological_sex = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    observations = relationship("HealthObservation", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    kb_version = Column(String(50), default="v2.0.0", nullable=False)
    status = Column(String(30), default="ACTIVE_INTAKE", nullable=False)  # ACTIVE_INTAKE, COMPLETED, EMERGENCY
    current_step = Column(String(30), default="DESCRIBE", nullable=False) # DESCRIBE, UNDERSTAND, CLARIFY, COMPLETED
    emergency_flagged = Column(Boolean, default=False, nullable=False)
    primary_complaint = Column(Text, nullable=False)
    reported_symptoms_json = Column(JSON, default=list, nullable=False)
    selected_locations_json = Column(JSON, default=list, nullable=False)
    properties_json = Column(JSON, default=dict, nullable=False)
    gemini_narrative = Column(Text, nullable=True)
    recommendation_tier = Column(String(50), default="ROUTINE", nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    user = relationship("User", back_populates="assessments")
    answers = relationship("AssessmentAnswer", back_populates="assessment", cascade="all, delete-orphan")
    conclusions = relationship("AssessmentConclusion", back_populates="assessment", cascade="all, delete-orphan")
    trace = relationship("AssessmentTrace", uselist=False, back_populates="assessment", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    fact_name = Column(String(150), nullable=False)
    value = Column(String(30), nullable=False)  # TRUE, FALSE, UNKNOWN, NOT_APPLICABLE
    raw_response = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    assessment = relationship("Assessment", back_populates="answers")

class AssessmentConclusion(Base):
    __tablename__ = "assessment_conclusions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    summary = Column(Text, nullable=False)
    recommendation_tier = Column(String(50), nullable=False)  # EMERGENCY, CONSULT_PHYSICIAN, SELF_MONITOR
    confidence = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    assessment = relationship("Assessment", back_populates="conclusions")

class AssessmentTrace(Base):
    __tablename__ = "assessment_traces"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), unique=True, nullable=False)
    trace_payload = Column(JSON, nullable=False)  # Contains full GraphPayload & execution steps
    execution_time_ms = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    assessment = relationship("Assessment", back_populates="trace")

class HealthObservation(Base):
    __tablename__ = "health_observations"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(String(36), nullable=True)
    title = Column(String(200), nullable=False)
    notes = Column(Text, nullable=True)
    severity = Column(String(30), default="MILD", nullable=False)  # MILD, MODERATE, SEVERE, CRITICAL
    recorded_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user = relationship("User", back_populates="observations")

class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    checksum_sha256 = Column(String(64), nullable=False)
    report_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    user = relationship("User", back_populates="reports")
    assessment = relationship("Assessment", back_populates="reports")

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), nullable=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(100), nullable=True)
    ip_address = Column(String(45), nullable=True)
    metadata_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)

