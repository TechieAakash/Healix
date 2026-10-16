from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.symptom import Symptom
from app.repositories.symptom_repository import SymptomRepository
from app.schemas.symptom import SymptomCreateRequest, SymptomUpdateRequest
from app.core.exceptions import EntityNotFoundException


class SymptomService:
    def __init__(self, db: Session):
        self.db = db
        self.symptom_repo = SymptomRepository(db)

    def create_symptom(self, user_id: str, req: SymptomCreateRequest) -> Symptom:
        symptom = Symptom(
            user_id=user_id,
            name=req.name,
            description=req.description,
            severity=req.severity,
            body_location=req.body_location,
            duration=req.duration,
            frequency=req.frequency,
        )
        return self.symptom_repo.create(symptom)

    def get_symptom(self, symptom_id: str, user_id: str) -> Symptom:
        symptom = self.symptom_repo.get_by_id_and_user(symptom_id, user_id)
        if not symptom:
            raise EntityNotFoundException("Symptom", symptom_id)
        return symptom

    def get_user_symptoms(self, user_id: str, page: int = 1, page_size: int = 20) -> Tuple[List[Symptom], int]:
        skip = (page - 1) * page_size
        items = self.symptom_repo.get_all_by_user(user_id, skip=skip, limit=page_size)
        total = self.symptom_repo.count_by_user(user_id)
        return items, total

    def update_symptom(self, symptom_id: str, user_id: str, req: SymptomUpdateRequest) -> Symptom:
        symptom = self.symptom_repo.get_by_id_and_user(symptom_id, user_id)
        if not symptom:
            raise EntityNotFoundException("Symptom", symptom_id)

        if req.name is not None:
            symptom.name = req.name
        if req.description is not None:
            symptom.description = req.description
        if req.severity is not None:
            symptom.severity = req.severity
        if req.body_location is not None:
            symptom.body_location = req.body_location
        if req.duration is not None:
            symptom.duration = req.duration
        if req.frequency is not None:
            symptom.frequency = req.frequency

        return self.symptom_repo.update(symptom)

    def delete_symptom(self, symptom_id: str, user_id: str) -> None:
        symptom = self.symptom_repo.get_by_id_and_user(symptom_id, user_id)
        if not symptom:
            raise EntityNotFoundException("Symptom", symptom_id)
        self.symptom_repo.delete(symptom)
