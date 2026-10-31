from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import init_db, AsyncSessionLocal
from .api.v1.api_router import api_router
from .repositories.repositories import UserRepository
from .db.models import User
from .core.security import hash_password

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    await init_db()
    
    # Seed demo user if not present
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        demo = await repo.get_by_email("demo@healix.ai")
        if not demo:
            demo_user = User(
                email="demo@healix.ai",
                password_hash=hash_password("HealixDemo2026!"),
                full_name="Ananya Sharma (Demo)",
                date_of_birth="2001-04-12",
                biological_sex="FEMALE"
            )
            await repo.create(demo_user)
            await session.commit()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Explainable AI Health Platform with Deterministic Production Rule Engine, Knowledge Graph, and NSUT AI Lab",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "HEALTHY",
        "platform": "Healix",
        "version": settings.VERSION,
        "engine": "Deterministic Production System v1.2.0"
    }

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Healix Explainable AI Health Platform API",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

