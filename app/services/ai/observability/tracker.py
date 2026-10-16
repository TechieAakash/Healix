"""
AI Observability and Audit Trail Tracker.
Records non-sensitive execution metrics, latency, token usage, retrieval statistics,
prompt versions, and safety validation statuses for every AI transaction.
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.core.config import settings

logger = logging.getLogger("healix.ai.observability")


class AIOperationAuditRecord(BaseModel):
    operation_id: str
    assessment_id: Optional[str] = None
    operation_type: str  # symptom_extraction, follow_up, rag_retrieval, symptom_analysis, summary, chat
    provider: str
    model: str
    prompt_version: str = Field(default=settings.PROMPT_VERSION)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    latency_ms: float
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
    retrieval_count: int = 0
    retrieved_document_ids: List[str] = Field(default_factory=list)
    validation_status: str = "SUCCESS"  # SUCCESS, SANITIZED, GROUNDING_WARNING, EMERGENCY_ENFORCED, FALLBACK
    fallback_used: bool = False
    error_type: Optional[str] = None


class AIObservabilityTracker:
    """
    Central recorder for all AI layer transactions.
    Ensures zero leak of raw sensitive medical text in audit logs while preserving total traceability.
    """

    def __init__(self, max_history: int = 500):
        self._history: List[AIOperationAuditRecord] = []
        self._max_history = max_history

    def record(
        self,
        operation_type: str,
        latency_ms: float,
        assessment_id: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        token_usage: Optional[Dict[str, int]] = None,
        retrieval_count: int = 0,
        retrieved_document_ids: Optional[List[str]] = None,
        validation_status: str = "SUCCESS",
        fallback_used: bool = False,
        error_type: Optional[str] = None,
    ) -> AIOperationAuditRecord:
        import uuid

        record = AIOperationAuditRecord(
            operation_id=str(uuid.uuid4()),
            assessment_id=assessment_id,
            operation_type=operation_type,
            provider=provider or settings.AI_PROVIDER,
            model=model or settings.AI_MODEL,
            prompt_version=settings.PROMPT_VERSION,
            latency_ms=round(latency_ms, 2),
            token_usage=token_usage or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            retrieval_count=retrieval_count,
            retrieved_document_ids=retrieved_document_ids or [],
            validation_status=validation_status,
            fallback_used=fallback_used,
            error_type=error_type,
        )

        self._history.append(record)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        # Structured audit log output (non-sensitive)
        logger.info(
            "AI_AUDIT op=%s assessment=%s latency=%.1fms tokens=%d docs=%d status=%s fallback=%s",
            record.operation_type,
            record.assessment_id or "none",
            record.latency_ms,
            record.token_usage.get("total_tokens", 0),
            record.retrieval_count,
            record.validation_status,
            record.fallback_used,
        )

        return record

    def get_recent_records(self, limit: int = 50) -> List[AIOperationAuditRecord]:
        return list(reversed(self._history[-limit:]))

    def get_records_by_assessment(self, assessment_id: str) -> List[AIOperationAuditRecord]:
        return [r for r in self._history if r.assessment_id == assessment_id]


# Global tracker singleton
ai_tracker = AIObservabilityTracker()
