from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.report import Report
from app.models.assessment import Assessment


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_and_user(self, report_id: str, user_id: str) -> Optional[Report]:
        stmt = (
            select(Report)
            .join(Assessment, Report.assessment_id == Assessment.id)
            .where(Report.id == report_id, Assessment.user_id == user_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_assessment_id(self, assessment_id: str) -> Optional[Report]:
        stmt = select(Report).where(Report.assessment_id == assessment_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all_by_user(self, user_id: str, skip: int = 0, limit: int = 20) -> List[Report]:
        stmt = (
            select(Report)
            .join(Assessment, Report.assessment_id == Assessment.id)
            .where(Assessment.user_id == user_id)
            .order_by(Report.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_by_user(self, user_id: str) -> int:
        stmt = (
            select(func.count(Report.id))
            .join(Assessment, Report.assessment_id == Assessment.id)
            .where(Assessment.user_id == user_id)
        )
        return self.db.execute(stmt).scalar() or 0

    def create(self, report: Report) -> Report:
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def delete(self, report: Report) -> None:
        self.db.delete(report)
        self.db.commit()
