"""
Unit & Integration Tests for Deterministic Python Health Engine.
Verifies negation handling, non-patient / hypothetical filtering,
ambiguous input safety, and symptom extraction accuracy without LLM.
"""

import pytest
from app.services.clinical.text_normalizer import clean_clinical_text, normalize_unicode
from app.services.clinical.negation_detector import negation_detector
from app.services.clinical.symptom_engine import symptom_engine
from app.services.triage_service import TriageService
from app.utils.constants import UrgencyLevel


def test_unicode_and_contraction_normalization():
    raw = "I’ve got a terrible headache—it won’t stop and I can’t sleep."
    cleaned = clean_clinical_text(raw)
    assert "i have" in cleaned
    assert "will not" in cleaned
    assert "cannot" in cleaned
    assert "—" not in cleaned


def test_negation_detection_explicit():
    # Negative cases
    assert negation_detector.is_negated("chest pain", "Patient reports no chest pain today") is True
    assert negation_detector.is_negated("shortness of breath", "Denies shortness of breath or fever") is True
    assert negation_detector.is_negated("fever", "Without any fever or chills") is True
    assert negation_detector.is_negated("coughing up blood", "Has not had any coughing up blood") is True

    # Positive cases
    assert negation_detector.is_negated("chest pain", "Patient reports severe chest pain radiating to arm") is False
    assert negation_detector.is_negated("headache", "Mild dull headache since yesterday") is False


def test_negation_contrastive_clauses():
    text = "No fever but severe headache and nausea"
    clauses = negation_detector.split_into_clauses(text)
    assert len(clauses) >= 2
    # "No fever" clause has negated fever
    assert negation_detector.is_negated("fever", clauses[0]) is True
    # "severe headache and nausea" clause does NOT have negated headache
    assert negation_detector.is_negated("headache", clauses[1]) is False


def test_hypothetical_and_third_party_context():
    clause1 = "What if my friend had severe chest pain?"
    assert negation_detector.is_third_party_or_hypothetical("chest pain", clause1) is True

    clause2 = "My mother has shortness of breath"
    assert negation_detector.is_third_party_or_hypothetical("shortness of breath", clause2) is True

    clause3 = "I have shortness of breath when walking"
    assert negation_detector.is_third_party_or_hypothetical("shortness of breath", clause3) is False


def test_triage_negated_emergency_does_not_trigger():
    """Crucial safety test: 'No chest pain' must NOT trigger cardiovascular emergency."""
    service = TriageService()
    result = service.evaluate(
        description="I have a mild headache. No chest pain and without shortness of breath.",
        symptoms=[{"name": "Headache", "severity": 3}],
    )
    assert result["urgency_level"] == UrgencyLevel.ROUTINE.value
    assert "RULE_CARDIO_001" not in result["triggered_rules"]
    assert "RULE_RESP_001" not in result["triggered_rules"]
    assert result["requires_professional_attention"] is False


def test_triage_hypothetical_does_not_trigger_emergency():
    """A user asking a hypothetical question about a family member should not trigger an emergency."""
    service = TriageService()
    result = service.evaluate(
        description="What if my friend experienced sudden chest pain? I just have a slight sore throat.",
        symptoms=[{"name": "Sore Throat", "severity": 2}],
    )
    assert result["urgency_level"] == UrgencyLevel.ROUTINE.value
    assert "RULE_CARDIO_001" not in result["triggered_rules"]


def test_triage_ambiguous_unknown_input():
    """Ambiguous or non-clinical text must return UNKNOWN, not falsely reassure with routine status."""
    service = TriageService()
    result = service.evaluate(
        description="I just feel completely weird and off today, not sure what is happening",
        symptoms=[],
    )
    assert result["urgency_level"] == UrgencyLevel.UNKNOWN.value
    assert "could not identify" in result["message"]
    assert result["is_ambiguous"] is True


def test_symptom_engine_multi_symptom_extraction():
    text = "I have had a throbbing head pounding since yesterday, feeling feverish and sick to my stomach."
    extracted = symptom_engine.extract(text)
    active = extracted["active_symptoms"]
    names = [s["canonical_name"] for s in active]

    assert "headache" in names
    assert "fever" in names
    assert "nausea" in names


def test_create_assessment_with_symptom_names(client, auth_headers):
    """Verify backend supports creating assessment with raw symptom names and auto-links them."""
    init_res = client.post(
        "/api/v1/assessments",
        headers=auth_headers,
        json={
            "description": "Feeling tired with a sore throat",
            "symptoms": ["Sore throat", "Fatigue"],
        },
    )
    assert init_res.status_code == 201
    assessment_id = init_res.json()["assessment_id"]

    # Verify assessment details have symptoms attached
    detail_res = client.get(f"/api/v1/assessments/{assessment_id}", headers=auth_headers)
    assert detail_res.status_code == 200
    symptoms = detail_res.json()["symptoms"]
    assert len(symptoms) >= 2
    sym_names = [s["name"].lower() for s in symptoms]
    assert any("throat" in n for n in sym_names)
    assert any("fatigue" in n for n in sym_names)
