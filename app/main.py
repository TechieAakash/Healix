from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import RequestLoggingMiddleware
from app.core.exceptions import (
    HealixException,
    healix_exception_handler,
    unhandled_exception_handler,
)
from app.api.routes import auth, users, symptoms, assessments, reports, chat, health
from app.core.database import Base, engine

# Initialize tables (for SQLite development fallback; Alembic handles production migrations)
if settings.DATABASE_URL.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
# Healix Healthcare Symptom Analysis & Triage Assistant API

**Healix** is an evidence-grounded symptom analysis and triage assistant.

### ⚠️ Clinical Disclaimer
Healix is **NOT a doctor** and does **NOT provide medical diagnosis**. 
All outputs are educational information and urgency guidelines to assist users in preparing for professional medical consultations.

### Features:
* 🔐 **Authentication**: Secure JWT access & refresh token authentication.
* 👤 **Patient Data Privacy**: IDOR-protected user profiles and data purge options.
* 🩺 **Symptom Tracker**: Structured severity (1-10) and duration recording.
* 📋 **Triage Workflow**: State-machine driven assessments with follow-up questioning.
* 🛡️ **Safety-First Engine**: Deterministic red-flag emergency screening rules.
* 🤖 **AI Grounding Layer**: Decoupled AI abstraction layer (Mock in Phase 1, ready for LLM & RAG in Phase 2).
* 📄 **Clinical Reports**: Appointment-ready medical brief generation.
* 💬 **Health Dialogue Assistant**: Conversational clinical Q&A.
    """,
    openapi_tags=[
        {"name": "Authentication", "description": "User registration, login, and JWT token rotation."},
        {"name": "Users", "description": "Patient profiles and GDPR/HIPAA privacy controls."},
        {"name": "Symptoms", "description": "Structured symptom cataloging and severity tracking."},
        {"name": "Assessments", "description": "Multi-step triage workflow and red-flag analysis."},
        {"name": "Reports", "description": "Doctor-ready medical summary briefs."},
        {"name": "Chat", "description": "Conversational healthcare assistant dialogues."},
        {"name": "Health", "description": "Service liveness and database connectivity checks."},
    ],
)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Structured Request Logging Middleware
app.add_middleware(RequestLoggingMiddleware)

# 3. Centralized Exception Handlers
app.add_exception_handler(HealixException, healix_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# 4. Include Routers
# Root Health endpoints
app.include_router(health.router)

# Versioned API routes under /api/v1
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(symptoms.router, prefix=settings.API_V1_STR)
app.include_router(assessments.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
