from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.report import Report
from app.repositories.report_repository import ReportRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.core.exceptions import EntityNotFoundException


class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.report_repo = ReportRepository(db)
        self.assessment_repo = AssessmentRepository(db)

    def get_report(self, report_id: str, user_id: str) -> Report:
        report = self.report_repo.get_by_id_and_user(report_id, user_id)
        if not report:
            raise EntityNotFoundException("Report", report_id)
        return report

    def list_reports(self, user_id: str, page: int = 1, page_size: int = 20) -> Tuple[List[Report], int]:
        skip = (page - 1) * page_size
        items = self.report_repo.get_all_by_user(user_id, skip=skip, limit=page_size)
        total = self.report_repo.count_by_user(user_id)
        return items, total

    def get_by_assessment_id(self, assessment_id: str, user_id: str) -> Report:
        assessment = self.assessment_repo.get_by_id_and_user(assessment_id, user_id)
        if not assessment:
            raise EntityNotFoundException("Assessment", assessment_id)
        report = self.report_repo.get_by_assessment_id(assessment_id)
        if not report:
            raise EntityNotFoundException("Report for Assessment", assessment_id)
        return report
