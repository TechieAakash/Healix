from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from ..db.models import (
    User, Assessment, AssessmentAnswer, AssessmentConclusion,
    AssessmentTrace, HealthObservation, Report, AuditEvent
)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        res = await self.db.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        res = await self.db.execute(select(User).where(User.id == user_id))
        return res.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

class AssessmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, assessment: Assessment) -> Assessment:
        self.db.add(assessment)
        await self.db.flush()
        return assessment

    async def get_by_id(self, assessment_id: str, user_id: str) -> Optional[Assessment]:
        res = await self.db.execute(
            select(Assessment).where(
                Assessment.id == assessment_id,
                Assessment.user_id == user_id
            )
        )
        return res.scalar_one_or_none()

    async def list_for_user(self, user_id: str, limit: int = 20) -> List[Assessment]:
        res = await self.db.execute(
            select(Assessment)
            .where(Assessment.user_id == user_id)
            .order_by(desc(Assessment.created_at))
            .limit(limit)
        )
        return list(res.scalars().all())

    async def save_answers(self, answers: List[AssessmentAnswer]):
        self.db.add_all(answers)
        await self.db.flush()

    async def save_conclusions(self, conclusions: List[AssessmentConclusion]):
        self.db.add_all(conclusions)
        await self.db.flush()

    async def save_trace(self, trace: AssessmentTrace):
        existing = await self.get_trace(trace.assessment_id)
        if existing:
            existing.trace_payload = trace.trace_payload
            existing.execution_time_ms = trace.execution_time_ms
        else:
            self.db.add(trace)
        await self.db.flush()

    async def get_conclusions(self, assessment_id: str) -> List[AssessmentConclusion]:
        res = await self.db.execute(
            select(AssessmentConclusion).where(AssessmentConclusion.assessment_id == assessment_id)
        )
        return list(res.scalars().all())

    async def get_trace(self, assessment_id: str) -> Optional[AssessmentTrace]:
        res = await self.db.execute(
            select(AssessmentTrace).where(AssessmentTrace.assessment_id == assessment_id)
        )
        return res.scalar_one_or_none()

class TimelineRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_observation(self, obs: HealthObservation) -> HealthObservation:
        self.db.add(obs)
        await self.db.flush()
        return obs

    async def list_observations(self, user_id: str, limit: int = 50) -> List[HealthObservation]:
        res = await self.db.execute(
            select(HealthObservation)
            .where(HealthObservation.user_id == user_id)
            .order_by(desc(HealthObservation.recorded_at))
            .limit(limit)
        )
        return list(res.scalars().all())

class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, report: Report) -> Report:
        self.db.add(report)
        await self.db.flush()
        return report

    async def get_by_id(self, report_id: str, user_id: str) -> Optional[Report]:
        res = await self.db.execute(
            select(Report).where(
                Report.id == report_id,
                Report.user_id == user_id
            )
        )
        return res.scalar_one_or_none()

    async def list_for_user(self, user_id: str, limit: int = 20) -> List[Report]:
        res = await self.db.execute(
            select(Report)
            .where(Report.user_id == user_id)
            .order_by(desc(Report.created_at))
            .limit(limit)
        )
        return list(res.scalars().all())

