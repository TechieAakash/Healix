"""
Clinical Symptom Registry and Ontology.
Structured clinical concepts mapped to standardized categories,
body locations, and common colloquial phrases.
"""

from typing import List, Dict, Any, Optional

SYMPTOM_CONCEPTS: List[Dict[str, Any]] = [
    {
        "id": "SYM_HEADACHE",
        "canonical_name": "headache",
        "category": "neurological",
        "default_location": "head",
        "aliases": [
            "headache", "head pain", "pain in head", "pain in my head",
            "my head hurts", "head hurts", "throbbing head", "head pounding",
            "temple pain", "cephalalgia", "migraine", "cranial pressure",
        ],
    },
    {
        "id": "SYM_CHEST_PAIN",
        "canonical_name": "chest pain",
        "category": "cardiovascular",
        "default_location": "chest",
        "aliases": [
            "chest pain", "chest tightness", "pressure on chest", "tight chest",
            "chest ache", "substernal pain", "chest pressure", "pain in my chest",
            "discomfort in chest", "heaviness in chest", "crushing chest pain",
        ],
    },
    {
        "id": "SYM_DYSPNEA",
        "canonical_name": "shortness of breath",
        "category": "respiratory",
        "default_location": "chest",
        "aliases": [
            "shortness of breath", "short of breath", "trouble breathing",
            "difficulty breathing", "cannot breathe", "can't catch breath",
            "breathless", "breathlessness", "winded", "hard to breathe",
            "gasping for air", "labored breathing",
        ],
    },
    {
        "id": "SYM_COUGH",
        "canonical_name": "cough",
        "category": "respiratory",
        "default_location": "throat/chest",
        "aliases": [
            "cough", "coughing", "hacking cough", "dry cough", "wet cough",
            "productive cough", "persistent cough", "barking cough",
        ],
    },
    {
        "id": "SYM_FEVER",
        "canonical_name": "fever",
        "category": "systemic_infectious",
        "default_location": "systemic",
        "aliases": [
            "fever", "running a fever", "feverish", "high temperature",
            "high temp", "chills", "fever and chills", "pyrexia", "hot and cold flashes",
        ],
    },
    {
        "id": "SYM_FATIGUE",
        "canonical_name": "fatigue",
        "category": "systemic_infectious",
        "default_location": "systemic",
        "aliases": [
            "fatigue", "tired", "exhausted", "exhaustion", "lethargy",
            "lethargic", "low energy", "worn out", "extreme tiredness",
            "malaise", "feeling drained",
        ],
    },
    {
        "id": "SYM_ABDO_PAIN",
        "canonical_name": "abdominal pain",
        "category": "gastrointestinal",
        "default_location": "abdomen",
        "aliases": [
            "abdominal pain", "stomach pain", "stomach hurts", "stomach ache", "belly ache",
            "belly pain", "tummy ache", "tummy pain", "gut pain",
            "stomach cramps", "abdominal cramps", "pain in stomach",
        ],
    },
    {
        "id": "SYM_NAUSEA",
        "canonical_name": "nausea",
        "category": "gastrointestinal",
        "default_location": "systemic/stomach",
        "aliases": [
            "nausea", "nauseous", "queasy", "sick to my stomach", "feeling sick",
            "upset stomach",
        ],
    },
    {
        "id": "SYM_VOMITING",
        "canonical_name": "vomiting",
        "category": "gastrointestinal",
        "default_location": "systemic/stomach",
        "aliases": [
            "vomiting", "vomited", "throwing up", "threw up", "puking",
            "emesis",
        ],
    },
    {
        "id": "SYM_SORE_THROAT",
        "canonical_name": "sore throat",
        "category": "respiratory",
        "default_location": "throat",
        "aliases": [
            "sore throat", "throat hurts", "throat is sore", "scratchy throat", "pain swallowing",
            "pharyngitis", "raw throat", "swollen throat",
        ],
    },
    {
        "id": "SYM_DIZZINESS",
        "canonical_name": "dizziness",
        "category": "neurological",
        "default_location": "head",
        "aliases": [
            "dizziness", "dizzy", "lightheaded", "lightheadedness", "woozy",
            "room spinning", "vertigo", "feeling faint", "unsteady",
        ],
    },
    {
        "id": "SYM_BODY_ACHE",
        "canonical_name": "body aches",
        "category": "musculoskeletal",
        "default_location": "systemic",
        "aliases": [
            "body aches", "body ache", "muscle aches", "myalgia", "aching all over",
            "sore muscles", "joint pain", "stiff joints",
        ],
    },
    {
        "id": "SYM_SKIN_RASH",
        "canonical_name": "skin rash",
        "category": "dermatological",
        "default_location": "skin",
        "aliases": [
            "skin rash", "rash", "red spots", "hives", "itchy skin",
            "urticaria", "skin irritation", "welts",
        ],
    },
    {
        "id": "SYM_BACK_PAIN",
        "canonical_name": "back pain",
        "category": "musculoskeletal",
        "default_location": "back",
        "aliases": [
            "back pain", "lower back pain", "lower back hurts", "upper back pain", "spine pain",
            "lumbar pain", "stiff back",
        ],
    },
    {
        "id": "SYM_DIARRHEA",
        "canonical_name": "diarrhea",
        "category": "gastrointestinal",
        "default_location": "abdomen",
        "aliases": [
            "diarrhea", "loose stools", "watery stools", "frequent stools",
            "upset bowel",
        ],
    },
]

# Quick lookup index by alias
ALIAS_TO_CONCEPT: Dict[str, Dict[str, Any]] = {}
for concept in SYMPTOM_CONCEPTS:
    for alias in concept["aliases"]:
        ALIAS_TO_CONCEPT[alias.lower()] = concept
