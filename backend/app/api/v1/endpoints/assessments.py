from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.database import get_db
from ....services.services import AssessmentService
from ....schemas.all_schemas import (
    StartAssessmentRequest, SubmitAdaptiveAnswerRequest,
    CreateAssessmentRequest, EvaluateAssessmentRequest,
    AssessmentSummaryItem
)
from ....db.models import User
from ..dependencies import get_current_user

router = APIRouter(prefix="/assessments", tags=["Assessments"])

@router.post("/start", status_code=status.HTTP_201_CREATED)
async def start_assessment(
    req: StartAssessmentRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Initializes a new multi-step assessment with primary complaint, symptom tags, and locations."""
    service = AssessmentService(db)
    assessment = await service.start_assessment(
        user_id=user.id,
        primary_complaint=req.primary_complaint,
        symptom_ids=req.symptom_ids,
        location_ids=req.location_ids,
        duration=req.duration,
        severity=req.severity,
        character=req.character
    )
    return {
        "assessment_id": assessment.id,
        "status": assessment.status,
        "current_step": assessment.current_step,
        "kb_version": assessment.kb_version,
        "primary_complaint": assessment.primary_complaint
    }

@router.get("/{assessment_id}/next-question")
async def get_next_question(
    assessment_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Fetches the next adaptive follow-up question based on currently known facts."""
    service = AssessmentService(db)
    return await service.get_next_question(assessment_id, user.id)

@router.post("/{assessment_id}/answer")
async def submit_question_answer(
    assessment_id: str,
    req: SubmitAdaptiveAnswerRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submits answer to an adaptive question and updates working memory facts."""
    service = AssessmentService(db)
    return await service.submit_answer(
        assessment_id=assessment_id,
        user_id=user.id,
        fact_name=req.fact_name,
        value=req.value,
        raw_response=req.raw_response
    )

@router.post("/{assessment_id}/complete")
async def complete_assessment(
    assessment_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Finalizes assessment, executes clinical reasoning engine, and generates Gemini narrative."""
    service = AssessmentService(db)
    return await service.complete_assessment(assessment_id, user.id)

# Legacy endpoints maintained for backwards compatibility
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_assessment_legacy(
    req: CreateAssessmentRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AssessmentService(db)
    assessment = await service.create_assessment(user.id, req.primary_complaint)
    return {
        "assessment_id": assessment.id,
        "status": assessment.status,
        "kb_version": assessment.kb_version,
        "primary_complaint": assessment.primary_complaint
    }

@router.post("/{assessment_id}/evaluate")
async def evaluate_assessment_legacy(
    assessment_id: str,
    req: EvaluateAssessmentRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AssessmentService(db)
    raw_answers = [a.model_dump() for a in req.answers]
    return await service.evaluate_assessment(assessment_id, user.id, raw_answers)

@router.get("", response_model=List[AssessmentSummaryItem])
async def list_assessments(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AssessmentService(db)
    items = await service.assessment_repo.list_for_user(user.id)
    summaries = []
    for item in items:
        concs = await service.assessment_repo.get_conclusions(item.id)
        top = concs[0].summary if concs else None
        summaries.append(
            AssessmentSummaryItem(
                id=item.id,
                primary_complaint=item.primary_complaint,
                status=item.status,
                emergency_flagged=item.emergency_flagged,
                top_conclusion=top,
                created_at=item.created_at.isoformat()
            )
        )
    return summaries

@router.get("/{assessment_id}")
async def get_assessment(
    assessment_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AssessmentService(db)
    assessment = await service.assessment_repo.get_by_id(assessment_id, user.id)
    if not assessment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    conclusions = await service.assessment_repo.get_conclusions(assessment_id)
    trace = await service.assessment_repo.get_trace(assessment_id)

    # Lookup rich metadata from clinical rules
    kb_meta: Dict[str, Any] = {}
    for rule in service.kb:
        for conc in rule.conclusions:
            kb_meta[conc.summary] = conc
            kb_meta[rule.id] = conc

    enriched_conclusions = []
    for c in conclusions:
        ref = kb_meta.get(c.summary, kb_meta.get(c.rule_id))
        detailed = ref.detailed_explanation if ref else "Symptom pattern evaluated against verified clinical policies. Outpatient consultation recommended if symptoms persist."
        steps = ref.actionable_steps if ref else [
            "Maintain an accurate symptom log tracking timing, intensity, and triggers.",
            "Schedule an outpatient evaluation with your primary care provider.",
            "Seek urgent emergency medical care (112 / 911) if acute warning signs develop."
        ]
        enriched_conclusions.append({
            "id": c.id,
            "rule_id": c.rule_id,
            "category": c.category,
            "summary": c.summary,
            "recommendation_tier": c.recommendation_tier,
            "confidence": c.confidence,
            "detailed_explanation": detailed,
            "actionable_steps": steps
        })

    return {
        "assessment_id": assessment.id,
        "status": assessment.status,
        "current_step": assessment.current_step,
        "emergency_flagged": assessment.emergency_flagged,
        "recommendation_tier": assessment.recommendation_tier,
        "kb_version": assessment.kb_version,
        "primary_complaint": assessment.primary_complaint,
        "reported_symptoms": assessment.reported_symptoms_json,
        "selected_locations": assessment.selected_locations_json,
        "properties": assessment.properties_json,
        "gemini_narrative": assessment.gemini_narrative,
        "created_at": assessment.created_at.isoformat(),
        "conclusions": enriched_conclusions,
        "has_trace": trace is not None
    }

@router.get("/{assessment_id}/graph")
async def get_assessment_graph(
    assessment_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AssessmentService(db)
    return await service.get_assessment_graph(assessment_id, user.id)

@router.post("/{assessment_id}/reports")
async def generate_report(
    assessment_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AssessmentService(db)
    report = await service.generate_report(assessment_id, user.id)
    return {
        "report_id": report.id,
        "title": report.title,
        "checksum_sha256": report.checksum_sha256,
        "report_data": report.report_data,
        "created_at": report.created_at.isoformat()
    }
