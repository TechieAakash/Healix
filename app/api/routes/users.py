from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserResponse, UserUpdateRequest
from app.schemas.common import MessageResponse
from app.services.user_service import UserService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the profile of the authenticated user. Prevents IDOR vulnerabilities.",
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_service = UserService(db)
    return user_service.get_user_profile(current_user.id)


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Updates name, date of birth, or gender for the current user.",
)
def update_current_user_profile(
    req: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.update_user_profile(current_user.id, req)


@router.delete(
    "/me",
    response_model=MessageResponse,
    summary="Delete current user account",
    description="Permanently deletes the authenticated user account and all associated health records.",
)
def delete_account(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user_service.delete_account(current_user.id)
    return MessageResponse(message="Account and all associated records permanently deleted.")


@router.delete(
    "/me/data",
    response_model=MessageResponse,
    summary="Purge user health records only",
    description="Deletes all recorded symptoms, assessments, and chat histories while preserving the user account.",
)
def purge_health_data(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user_service.delete_health_data_only(current_user.id)
    return MessageResponse(message="All health records and assessments have been wiped.")
