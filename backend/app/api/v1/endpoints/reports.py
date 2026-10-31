from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.database import get_db
from ....repositories.repositories import ReportRepository
from ....schemas.all_schemas import ReportResponse
from ....db.models import User
from ..dependencies import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("", response_model=List[ReportResponse])
async def list_reports(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ReportRepository(db)
    items = await repo.list_for_user(user.id)
    return [
        ReportResponse(
            id=item.id,
            assessment_id=item.assessment_id,
            title=item.title,
            checksum_sha256=item.checksum_sha256,
            created_at=item.created_at.isoformat(),
            report_data=item.report_data
        )
        for item in items
    ]

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ReportRepository(db)
    item = await repo.get_by_id(report_id, user.id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return ReportResponse(
        id=item.id,
        assessment_id=item.assessment_id,
        title=item.title,
        checksum_sha256=item.checksum_sha256,
        created_at=item.created_at.isoformat(),
        report_data=item.report_data
    )

