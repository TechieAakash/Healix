from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from app.schemas.user import UserResponse
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user, login_rate_limiter
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new patient account",
    description="Registers a new user with email, name, password, and optional demographic data.",
)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register(req)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and obtain JWT tokens",
    description="Authenticates via email and password, returning JWT access and refresh tokens.",
    dependencies=[Depends(login_rate_limiter)],
)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.login(req)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Validates a refresh token and returns a new access/refresh token pair.",
)
def refresh_token(req: RefreshTokenRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.refresh(req.refresh_token)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Log out active session",
    description="Client clears token. Future Redis integration will handle token denylisting.",
)
def logout(current_user: User = Depends(get_current_user)):
    return MessageResponse(message="Successfully logged out.")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get authenticated user identity",
    description="Returns the profile of the currently authenticated user.",
)
def get_auth_me(current_user: User = Depends(get_current_user)):
    return current_user
