from typing import List, Tuple, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.assessment import Assessment
from app.models.follow_up import FollowUpQuestion, FollowUpAnswer
from app.models.report import Report
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.symptom_repository import SymptomRepository
from app.repositories.report_repository import ReportRepository
from app.services.triage_service import TriageService
from app.services.ai_service import AIService, MockAIService, get_ai_service
from app.schemas.assessment import AssessmentCreateRequest, AssessmentAnalyzeResponse
from app.core.exceptions import (
    EntityNotFoundException,
    InvalidAssessmentStateException,
    ForbiddenException,
)
from app.utils.constants import AssessmentStatus, UrgencyLevel, QuestionType, STANDARD_MEDICAL_DISCLAIMER


class AssessmentService:
    def __init__(self, db: Session, ai_service: Optional[AIService] = None):
        self.db = db
        self.assessment_repo = AssessmentRepository(db)
        self.symptom_repo = SymptomRepository(db)
        self.report_repo = ReportRepository(db)
        self.triage_service = TriageService()
        self.ai_service = ai_service or get_ai_service()

    def create_assessment(self, user_id: str, req: AssessmentCreateRequest) -> Assessment:
        # Load and verify attached symptoms
        symptoms = []
        if req.symptoms:
            symptoms = self.symptom_repo.get_by_ids_and_user(req.symptoms, user_id)

        assessment = Assessment(
            user_id=user_id,
            status=AssessmentStatus.SYMPTOMS_COLLECTED.value,
            urgency_level=UrgencyLevel.UNKNOWN.value,
            user_description=req.description,
            symptoms=symptoms,
        )
        return self.assessment_repo.create(assessment)

    def get_assessment(self, assessment_id: str, user_id: str) -> Assessment:
        assessment = self.assessment_repo.get_by_id_and_user(assessment_id, user_id)
        if not assessment:
            raise EntityNotFoundException("Assessment", assessment_id)
        return assessment

    def list_assessments(self, user_id: str, page: int = 1, page_size: int = 20) -> Tuple[List[Assessment], int]:
        skip = (page - 1) * page_size
        items = self.assessment_repo.get_all_by_user(user_id, skip=skip, limit=page_size)
        total = self.assessment_repo.count_by_user(user_id)
        return items, total

    async def get_or_generate_questions(self, assessment_id: str, user_id: str) -> List[FollowUpQuestion]:
        assessment = self.get_assessment(assessment_id, user_id)

        # Return existing questions if already generated
        if assessment.follow_up_questions:
            return assessment.follow_up_questions

        # Generate through AI abstraction
        symptoms_data = [
            {"name": s.name, "severity": s.severity, "description": s.description}
            for s in assessment.symptoms
        ]
        q_dicts = await self.ai_service.generate_follow_up_questions(
            assessment.user_description or "", symptoms_data
        )

        question_entities = [
            FollowUpQuestion(
                assessment_id=assessment.id,
                question=q["question"],
                question_type=q.get("type", QuestionType.SINGLE_CHOICE.value),
                order_index=q.get("order_index", idx),
            )
            for idx, q in enumerate(q_dicts)
        ]

        saved_questions = self.assessment_repo.create_follow_up_questions(question_entities)
        assessment.status = AssessmentStatus.FOLLOW_UP.value
        self.assessment_repo.update(assessment)
        return saved_questions

    def answer_question(
        self, assessment_id: str, question_id: str, user_id: str, answer_text: str
    ) -> FollowUpAnswer:
        assessment = self.get_assessment(assessment_id, user_id)
        question = self.assessment_repo.get_question_by_id_and_assessment(question_id, assessment.id)
        if not question:
            raise EntityNotFoundException("FollowUpQuestion", question_id)

        answer = FollowUpAnswer(question_id=question.id, answer=answer_text)
        return self.assessment_repo.create_follow_up_answer(answer)

    async def analyze_assessment(self, assessment_id: str, user_id: str) -> AssessmentAnalyzeResponse:
        assessment = self.get_assessment(assessment_id, user_id)

        # Update state to ANALYZING
        assessment.status = AssessmentStatus.ANALYZING.value
        self.assessment_repo.update(assessment)

        # Gather context
        symptoms_data = [
            {
                "name": s.name,
                "severity": s.severity,
                "description": s.description,
                "location": s.body_location,
            }
            for s in assessment.symptoms
        ]
        answers_data = [
            {"question": q.question, "answer": a.answer}
            for q in assessment.follow_up_questions
            for a in q.answers
        ]

        # STEP 1: Run Deterministic Red-Flag Triage Engine FIRST
        triage_result = self.triage_service.evaluate(
            description=assessment.user_description or "",
            symptoms=symptoms_data,
            answers=answers_data,
        )

        # STEP 2: Generate Evidence-Grounded Summary via AI Service
        summary_result = await self.ai_service.generate_summary(
            description=assessment.user_description or "",
            symptoms=symptoms_data,
            answers=answers_data,
            triage_result=triage_result,
            assessment_id=assessment.id,
        )

        # STEP 3: Create and Save Clinical Report
        primary_symptom = assessment.symptoms[0].name if assessment.symptoms else "Health Assessment"
        report = Report(
            assessment_id=assessment.id,
            title=f"Assessment Report: {primary_symptom}",
            summary=summary_result["summary"],
            urgency_level=triage_result["urgency_level"],
            possible_explanations=summary_result["possible_explanations"],
            general_guidance=summary_result["general_guidance"],
            warning_signs=summary_result["warning_signs"],
            sources=summary_result["sources"],
        )
        self.report_repo.create(report)

        # STEP 4: Mark assessment COMPLETED
        assessment.status = AssessmentStatus.COMPLETED.value
        assessment.urgency_level = triage_result["urgency_level"]
        assessment.summary = summary_result["summary"]
        self.assessment_repo.update(assessment)

        return AssessmentAnalyzeResponse(
            assessment_id=assessment.id,
            urgency_level=triage_result["urgency_level"],
            summary=summary_result["summary"],
            possible_explanations=summary_result["possible_explanations"],
            general_guidance=summary_result["general_guidance"],
            warning_signs=summary_result["warning_signs"],
            sources=summary_result["sources"],
            disclaimer=STANDARD_MEDICAL_DISCLAIMER,
        )
