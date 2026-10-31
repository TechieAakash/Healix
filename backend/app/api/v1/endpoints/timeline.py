from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.database import get_db
from ....repositories.repositories import TimelineRepository
from ....schemas.all_schemas import CreateObservationRequest, ObservationResponse
from ....db.models import User, HealthObservation
from ..dependencies import get_current_user

router = APIRouter(prefix="/timeline", tags=["Timeline"])

@router.get("", response_model=List[ObservationResponse])
async def list_timeline_observations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = TimelineRepository(db)
    items = await repo.list_observations(user.id)
    return [
        ObservationResponse(
            id=item.id,
            user_id=item.user_id,
            assessment_id=item.assessment_id,
            title=item.title,
            notes=item.notes,
            severity=item.severity,
            recorded_at=item.recorded_at.isoformat()
        )
        for item in items
    ]

@router.post("", response_model=ObservationResponse, status_code=status.HTTP_201_CREATED)
async def create_observation(
    req: CreateObservationRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = TimelineRepository(db)
    obs = HealthObservation(
        user_id=user.id,
        assessment_id=req.assessment_id,
        title=req.title,
        notes=req.notes,
        severity=req.severity
    )
    saved = await repo.create_observation(obs)
    return ObservationResponse(
        id=saved.id,
        user_id=saved.user_id,
        assessment_id=saved.assessment_id,
        title=saved.title,
        notes=saved.notes,
        severity=saved.severity,
        recorded_at=saved.recorded_at.isoformat()
    )

