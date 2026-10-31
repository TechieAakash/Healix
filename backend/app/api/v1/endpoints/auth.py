from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.database import get_db
from ....services.services import AuthService
from ....schemas.all_schemas import RegisterRequest, LoginRequest, AuthResponse, UserProfileResponse
from ....db.models import User
from ..dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register(
        email=req.email,
        password=req.password,
        full_name=req.full_name,
        dob=req.date_of_birth,
        sex=req.biological_sex
    )

@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(email=req.email, password=req.password)

@router.get("/me", response_model=UserProfileResponse)
async def get_me(user: User = Depends(get_current_user)):
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        date_of_birth=user.date_of_birth,
        biological_sex=user.biological_sex,
        created_at=user.created_at.isoformat()
    )

