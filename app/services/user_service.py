from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdateRequest
from app.core.exceptions import EntityNotFoundException


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_user_profile(self, user_id: str) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)
        return user

    def update_user_profile(self, user_id: str, req: UserUpdateRequest) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        if req.name is not None:
            user.name = req.name
        if req.date_of_birth is not None:
            user.date_of_birth = req.date_of_birth
        if req.gender is not None:
            user.gender = req.gender

        return self.user_repo.update(user)

    def delete_account(self, user_id: str) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)
        # Cascade deletes all symptoms, assessments, reports, conversations
        self.user_repo.delete(user)

    def delete_health_data_only(self, user_id: str) -> None:
        """
        Deletes all health data (symptoms, assessments, conversations)
        while preserving the active user account for data privacy compliance.
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        # Clear relationships
        user.symptoms.clear()
        user.assessments.clear()
        user.conversations.clear()
        self.db.commit()
