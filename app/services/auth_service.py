from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.config import settings
from app.core.exceptions import (
    DuplicateEntityException,
    UnauthorizedException,
    HealixException,
)
from app.utils.validators import validate_password_strength


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, req: UserRegisterRequest) -> User:
        # Validate password strength
        is_valid, msg = validate_password_strength(req.password)
        if not is_valid:
            raise HealixException(code="WEAK_PASSWORD", message=msg)

        # Check existing email
        existing = self.user_repo.get_by_email(req.email)
        if existing:
            raise DuplicateEntityException("User", "email", req.email)

        # Create user
        user = User(
            name=req.name,
            email=req.email.lower().strip(),
            password_hash=get_password_hash(req.password),
            date_of_birth=req.date_of_birth,
            gender=req.gender,
            is_active=True,
        )
        return self.user_repo.create(user)

    def login(self, req: UserLoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_email(req.email.lower().strip())
        if not user or not user.is_active:
            raise UnauthorizedException("Incorrect email or password")

        if not verify_password(req.password, user.password_hash):
            raise UnauthorizedException("Incorrect email or password")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token")

        user_id = payload.get("sub")
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        new_access = create_access_token(user.id)
        new_refresh = create_refresh_token(user.id)

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
