from typing import Any, Optional, Dict
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class HealixException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class EntityNotFoundException(HealixException):
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            code=f"{entity_name.upper()}_NOT_FOUND",
            message=f"{entity_name} with id {entity_id} was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UnauthorizedException(HealixException):
    def __init__(self, message: str = "Invalid or expired credentials"):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenException(HealixException):
    def __init__(self, message: str = "You do not have permission to access this resource"):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class DuplicateEntityException(HealixException):
    def __init__(self, entity_name: str, field_name: str, value: Any):
        super().__init__(
            code=f"{entity_name.upper()}_ALREADY_EXISTS",
            message=f"{entity_name} with {field_name} '{value}' already exists.",
            status_code=status.HTTP_409_CONFLICT,
        )


class InvalidAssessmentStateException(HealixException):
    def __init__(self, current_state: str, action: str):
        super().__init__(
            code="INVALID_ASSESSMENT_STATE",
            message=f"Cannot perform action '{action}' on assessment in state '{current_state}'.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class AnalysisFailedException(HealixException):
    def __init__(self, message: str = "Triage analysis could not be completed."):
        super().__init__(
            code="ANALYSIS_FAILED",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class RateLimitExceededException(HealixException):
    def __init__(self, limit_desc: str = "Too many requests. Please try again later."):
        super().__init__(
            code="RATE_LIMIT_EXCEEDED",
            message=limit_desc,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


class ValidationException(HealixException):
    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class AIException(HealixException):
    def __init__(self, message: str = "AI service error", status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(
            code="AI_SERVICE_ERROR",
            message=message,
            status_code=status_code,
        )


async def healix_exception_handler(request: Request, exc: HealixException) -> JSONResponse:
    content = {
        "error": {
            "code": exc.code,
            "message": exc.message,
        }
    }
    if exc.details:
        content["error"]["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content=content)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please contact support.",
            }
        },
    )
