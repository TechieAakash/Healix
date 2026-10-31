from fastapi import APIRouter
from .endpoints import auth, assessments, timeline, reports, rules, symptoms

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(symptoms.router)
api_router.include_router(assessments.router)
api_router.include_router(timeline.router)
api_router.include_router(reports.router)
api_router.include_router(rules.router)
