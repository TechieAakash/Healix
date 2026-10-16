from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
