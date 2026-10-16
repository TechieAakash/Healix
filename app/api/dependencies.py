import time
from typing import Generator, Optional, Dict
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, RateLimitExceededException
from app.repositories.user_repository import UserRepository
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    if not token:
        raise UnauthorizedException("Authentication token is missing")

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException("Could not validate credentials or token expired")

    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise UnauthorizedException("User no longer exists")
    if not user.is_active:
        raise UnauthorizedException("User account is disabled")

    return user


class InMemoryRateLimiter:
    """
    In-memory rate limiter with sliding window by client IP.
    Designed so that a Redis-backed RateLimiter can easily drop in later.
    """

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window = 60  # seconds
        self.history: Dict[str, list] = {}

    def __call__(self, request: Request):
        # Identify by client IP
        client_host = request.client.host if request.client else "unknown_client"
        endpoint = request.url.path
        key = f"{client_host}:{endpoint}"
        now = time.time()

        # Purge records older than 1 minute
        if key not in self.history:
            self.history[key] = []
        self.history[key] = [t for t in self.history[key] if now - t < self.window]

        if len(self.history[key]) >= self.requests_per_minute:
            raise RateLimitExceededException(
                f"Rate limit exceeded: maximum {self.requests_per_minute} requests per minute."
            )

        self.history[key].append(now)


# Standard rate limiting dependency instances
login_rate_limiter = InMemoryRateLimiter(requests_per_minute=20)
analysis_rate_limiter = InMemoryRateLimiter(requests_per_minute=30)
chat_rate_limiter = InMemoryRateLimiter(requests_per_minute=60)
