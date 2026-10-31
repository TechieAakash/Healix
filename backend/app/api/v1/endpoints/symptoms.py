from typing import List, Dict, Any
from fastapi import APIRouter
from ....clinical_engine.symptoms import SYMPTOM_CATALOGUE, ANATOMICAL_LOCATIONS, find_symptom_by_text
from ....schemas.all_schemas import ParseSymptomsRequest, ParseSymptomsResponse
from ....services.gemini_service import GeminiService

router = APIRouter(prefix="/symptoms", tags=["Symptoms Catalogue & NLP"])
gemini_service = GeminiService()

@router.get("/catalog")
async def get_symptom_catalog():
    """Returns the versioned catalogue of supported symptoms and anatomical regions."""
    return {
        "version": "2.0.0",
        "total_symptoms": len(SYMPTOM_CATALOGUE),
        "symptoms": [s.model_dump() for s in SYMPTOM_CATALOGUE],
        "anatomical_locations": [l.model_dump() for l in ANATOMICAL_LOCATIONS]
    }

@router.post("/parse", response_model=ParseSymptomsResponse)
async def parse_symptom_text(req: ParseSymptomsRequest):
    """Parses free-text natural language symptom descriptions into structured clinical entities."""
    return await gemini_service.parse_symptom_description(req.free_text)

