from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from app.models.assessment import Assessment
from app.models.follow_up import FollowUpQuestion, FollowUpAnswer


class AssessmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_and_user(self, assessment_id: str, user_id: str) -> Optional[Assessment]:
        stmt = (
            select(Assessment)
            .options(
                selectinload(Assessment.symptoms),
                selectinload(Assessment.follow_up_questions).selectinload(FollowUpQuestion.answers),
                selectinload(Assessment.report),
            )
            .where(Assessment.id == assessment_id, Assessment.user_id == user_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all_by_user(self, user_id: str, skip: int = 0, limit: int = 20) -> List[Assessment]:
        stmt = (
            select(Assessment)
            .options(
                selectinload(Assessment.symptoms),
                selectinload(Assessment.report),
            )
            .where(Assessment.user_id == user_id)
            .order_by(Assessment.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_by_user(self, user_id: str) -> int:
        stmt = select(func.count(Assessment.id)).where(Assessment.user_id == user_id)
        return self.db.execute(stmt).scalar() or 0

    def create(self, assessment: Assessment) -> Assessment:
        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def update(self, assessment: Assessment) -> Assessment:
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def delete(self, assessment: Assessment) -> None:
        self.db.delete(assessment)
        self.db.commit()

    def create_follow_up_questions(self, questions: List[FollowUpQuestion]) -> List[FollowUpQuestion]:
        self.db.add_all(questions)
        self.db.commit()
        for q in questions:
            self.db.refresh(q)
        return questions

    def get_question_by_id_and_assessment(self, question_id: str, assessment_id: str) -> Optional[FollowUpQuestion]:
        stmt = select(FollowUpQuestion).where(
            FollowUpQuestion.id == question_id,
            FollowUpQuestion.assessment_id == assessment_id,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_follow_up_answer(self, answer: FollowUpAnswer) -> FollowUpAnswer:
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer
