from typing import List, Dict, Any
from fastapi import APIRouter
from ....engine.knowledge_base.rules_data import get_clinical_knowledge_base, KB_VERSION

router = APIRouter(prefix="/rules", tags=["Knowledge Base Rules"])

@router.get("")
async def list_rules():
    rules = get_clinical_knowledge_base()
    return {
        "kb_version": KB_VERSION,
        "total_rules": len(rules),
        "rules": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "priority": r.priority,
                "category": r.category.value,
                "provenance": r.provenance,
                "version": r.version,
                "specificity": r.get_specificity_score(),
                "required_facts": r.get_all_required_facts(),
                "conclusions": [c.model_dump(mode="json") for c in r.conclusions]
            }
            for r in rules
        ]
    }

