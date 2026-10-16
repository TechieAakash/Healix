from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.assessment import (
    AssessmentCreateRequest,
    AssessmentResponse,
    AssessmentInitResponse,
    AssessmentAnalyzeResponse,
)
from app.schemas.follow_up import (
    FollowUpQuestionsListResponse,
    FollowUpAnswerRequest,
    FollowUpAnswerResponse,
    FollowUpQuestionItem,
)
from app.schemas.common import PaginatedResponse
from app.services.assessment_service import AssessmentService
from app.api.dependencies import get_current_user, analysis_rate_limiter
from app.models.user import User

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post(
    "",
    response_model=AssessmentInitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Initialize health assessment",
    description="Creates a new symptom assessment session and links selected symptom records.",
)
def create_assessment(
    req: AssessmentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssessmentService(db)
    assessment = service.create_assessment(current_user.id, req)
    return AssessmentInitResponse(assessment_id=assessment.id, status=assessment.status)


@router.get(
    "",
    response_model=PaginatedResponse[AssessmentResponse],
    summary="List patient assessments",
    description="Returns a paginated timeline of health assessments created by the authenticated user.",
)
def list_assessments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssessmentService(db)
    items, total = service.list_assessments(current_user.id, page=page, page_size=page_size)
    return PaginatedResponse(items=items, page=page, page_size=page_size, total=total)


@router.get(
    "/{id}",
    response_model=AssessmentResponse,
    summary="Get assessment details",
    description="Fetches full assessment details, symptoms, questions, and attached report.",
)
def get_assessment(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssessmentService(db)
    return service.get_assessment(id, current_user.id)


@router.post(
    "/{id}/questions",
    response_model=FollowUpQuestionsListResponse,
    summary="Generate or retrieve follow-up triage questions",
    description="Retrieves or generates context-aware follow-up questions to refine clinical intake.",
)
async def get_follow_up_questions(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssessmentService(db)
    questions = await service.get_or_generate_questions(id, current_user.id)
    items = [
        FollowUpQuestionItem(
            id=q.id,
            question=q.question,
            type=q.question_type,
            order_index=q.order_index,
        )
        for q in questions
    ]
    return FollowUpQuestionsListResponse(questions=items)


@router.post(
    "/{id}/answers",
    response_model=FollowUpAnswerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit answer to a follow-up question",
    description="Records user response to an assessment follow-up question.",
)
def submit_follow_up_answer(
    id: str,
    req: FollowUpAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssessmentService(db)
    answer = service.answer_question(id, req.question_id, current_user.id, req.answer)
    return FollowUpAnswerResponse(
        id=answer.id,
        question_id=answer.question_id,
        answer=answer.answer,
        created_at=answer.created_at,
    )


@router.post(
    "/{id}/analyze",
    response_model=AssessmentAnalyzeResponse,
    summary="Execute triage analysis & generate report",
    description="Runs the safety-first triage rules, queries evidence via AI service, and generates a structured clinical report.",
    dependencies=[Depends(analysis_rate_limiter)],
)
async def analyze_assessment(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssessmentService(db)
    return await service.analyze_assessment(id, current_user.id)
