from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.symptom import SymptomCreateRequest, SymptomUpdateRequest, SymptomResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.symptom_service import SymptomService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/symptoms", tags=["Symptoms"])


@router.post(
    "",
    response_model=SymptomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a new symptom",
    description="Logs a symptom with name, severity (1-10), body location, duration, and frequency.",
)
def create_symptom(
    req: SymptomCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SymptomService(db)
    return service.create_symptom(current_user.id, req)


@router.get(
    "",
    response_model=PaginatedResponse[SymptomResponse],
    summary="List user symptoms",
    description="Returns a paginated list of symptoms recorded by the authenticated user.",
)
def list_symptoms(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SymptomService(db)
    items, total = service.get_user_symptoms(current_user.id, page=page, page_size=page_size)
    return PaginatedResponse(items=items, page=page, page_size=page_size, total=total)


@router.get(
    "/{id}",
    response_model=SymptomResponse,
    summary="Get symptom by ID",
    description="Fetches a specific symptom record belonging to the authenticated user.",
)
def get_symptom(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SymptomService(db)
    return service.get_symptom(id, current_user.id)


@router.patch(
    "/{id}",
    response_model=SymptomResponse,
    summary="Update symptom details",
    description="Updates severity, description, frequency, or duration of a recorded symptom.",
)
def update_symptom(
    id: str,
    req: SymptomUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SymptomService(db)
    return service.update_symptom(id, current_user.id, req)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Delete a symptom record",
    description="Deletes a recorded symptom belonging to the authenticated user.",
)
def delete_symptom(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SymptomService(db)
    service.delete_symptom(id, current_user.id)
    return MessageResponse(message="Symptom record deleted successfully.")
