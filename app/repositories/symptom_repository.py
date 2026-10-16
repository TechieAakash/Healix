from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.symptom import Symptom


class SymptomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_and_user(self, symptom_id: str, user_id: str) -> Optional[Symptom]:
        stmt = select(Symptom).where(Symptom.id == symptom_id, Symptom.user_id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all_by_user(self, user_id: str, skip: int = 0, limit: int = 20) -> List[Symptom]:
        stmt = (
            select(Symptom)
            .where(Symptom.user_id == user_id)
            .order_by(Symptom.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_by_user(self, user_id: str) -> int:
        stmt = select(func.count(Symptom.id)).where(Symptom.user_id == user_id)
        return self.db.execute(stmt).scalar() or 0

    def get_by_ids_and_user(self, symptom_ids: List[str], user_id: str) -> List[Symptom]:
        if not symptom_ids:
            return []
        stmt = select(Symptom).where(Symptom.id.in_(symptom_ids), Symptom.user_id == user_id)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, symptom: Symptom) -> Symptom:
        self.db.add(symptom)
        self.db.commit()
        self.db.refresh(symptom)
        return symptom

    def update(self, symptom: Symptom) -> Symptom:
        self.db.commit()
        self.db.refresh(symptom)
        return symptom

    def delete(self, symptom: Symptom) -> None:
        self.db.delete(symptom)
        self.db.commit()
