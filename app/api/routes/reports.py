from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.report import ReportResponse
from app.schemas.common import PaginatedResponse
from app.services.report_service import ReportService
from app.services.assessment_service import AssessmentService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "",
    response_model=PaginatedResponse[ReportResponse],
    summary="List patient medical summary reports",
    description="Returns a paginated list of generated clinical intake reports for the authenticated user.",
)
def list_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ReportService(db)
    items, total = service.list_reports(current_user.id, page=page, page_size=page_size)
    return PaginatedResponse(items=items, page=page, page_size=page_size, total=total)


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Get clinical report by ID",
    description="Retrieves a specific medical brief. Enforces strict user authorization.",
)
def get_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ReportService(db)
    return service.get_report(report_id, current_user.id)


@router.post(
    "/{assessment_id}/generate",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate report from assessment",
    description="Analyzes assessment and generates a report if one does not already exist.",
)
async def generate_report_for_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assessment_service = AssessmentService(db)
    await assessment_service.analyze_assessment(assessment_id, current_user.id)
    report_service = ReportService(db)
    return report_service.get_by_assessment_id(assessment_id, current_user.id)
