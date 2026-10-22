"""Small, explicit symptom ``isa`` hierarchy used by extraction and safety rules."""

from typing import Dict, Iterable, Set


ISA_PARENTS: Dict[str, str] = {
    "chest_pressure": "chest_pain",
    "chest_pain": "cardiovascular_symptom",
    "shortness_of_breath": "respiratory_symptom",
    "cough": "respiratory_symptom",
    "sore_throat": "respiratory_symptom",
    "headache": "neurological_symptom",
    "dizziness": "neurological_symptom",
    "abdominal_pain": "gastrointestinal_symptom",
    "nausea": "gastrointestinal_symptom",
    "vomiting": "gastrointestinal_symptom",
    "diarrhea": "gastrointestinal_symptom",
    "fever": "systemic_symptom",
    "fatigue": "systemic_symptom",
}


def concept_key(value: str) -> str:
    return "_".join(str(value or "").strip().casefold().replace("-", " ").split())


def ancestors(concept: str) -> Set[str]:
    """Return transitive parent concepts for a normalized symptom concept."""
    result: Set[str] = set()
    current = concept_key(concept)
    while current in ISA_PARENTS and ISA_PARENTS[current] not in result:
        current = ISA_PARENTS[current]
        result.add(current)
    return result


def is_a(concept: str, parent: str) -> bool:
    child_key, parent_key = concept_key(concept), concept_key(parent)
    return child_key == parent_key or parent_key in ancestors(child_key)


def ontology_facts(concept: str) -> Iterable[str]:
    """Yield parent concepts for a symptom; useful to evidence and rule mappers."""
    return sorted(ancestors(concept))
