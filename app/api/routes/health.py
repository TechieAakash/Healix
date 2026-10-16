from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Service liveness health check",
    description="Returns service health status.",
)
def health_check():
    return {"status": "healthy"}


@router.get(
    "/health/db",
    summary="Database connectivity check",
    description="Executes a ping query to verify database connection availability.",
)
def database_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return Response(
            content='{"status": "unhealthy", "database": "disconnected"}',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json",
        )
