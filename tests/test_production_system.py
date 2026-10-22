from app.services.triage_service import RED_FLAG_RULES, TriageService
from app.services.clinical.symptom_ontology import is_a
from app.utils.constants import UrgencyLevel


def test_rules_have_explicit_production_fields():
    for rule in RED_FLAG_RULES:
        assert rule["id"]
        assert rule["conditions"]
        assert rule["conclusion"]
        assert rule["urgency"]
        assert rule["source"]
        assert rule["reference"]


def test_ontology_parent_condition_matches_child_symptom():
    result = TriageService().evaluate("I feel chest pressure")
    assert is_a("chest_pressure", "cardiovascular_symptom")
    assert result["urgency_level"] == UrgencyLevel.EMERGENCY.value
    cardio = next(item for item in result["reasoning_trace"] if item["rule_id"] == "RULE_CARDIO_001")
    assert any(fact["predicate"] == "isa" and fact["value"] == "cardiovascular_symptom" for fact in cardio["matched_facts"])


def test_negated_and_hypothetical_findings_do_not_fire_rules():
    service = TriageService()
    negated = service.evaluate("I have no chest pain")
    hypothetical = service.evaluate("What if I had chest pain? I would call a doctor")
    assert "RULE_CARDIO_001" not in negated["triggered_rules"]
    assert "RULE_CARDIO_001" not in hypothetical["triggered_rules"]
    assert negated["reasoning_trace"] == []


def test_backward_chaining_prioritizes_unknown_red_flags_for_relevant_context():
    result = TriageService().evaluate("I have had a headache for two days")
    assert result["urgency_level"] == UrgencyLevel.ROUTINE.value
    question = next(q for q in result["priority_questions"] if q["rule_id"] == "RULE_NEURO_001")
    assert question["unknown_facts"]
    assert question["reasoning"]
    assert "suddenly" in question["question"]


def test_established_emergency_bypasses_confirmation_questions():
    result = TriageService().evaluate("I have sudden facial drooping and slurred speech")
    assert result["urgency_level"] == UrgencyLevel.EMERGENCY.value
    assert result["priority_questions"] == []
    assert result["reasoning_trace"][0]["source"]


def test_working_memory_tracks_structured_fields_and_unknowns():
    result = TriageService().evaluate(
        "My knee hurts",
        symptoms=[{"name": "Knee pain", "severity": 6, "duration": "3 days", "age": 72, "sex": "F"}],
    )
    facts = result["working_memory"]
    assert any(f["predicate"] == "severity" and f["value"] == 6 for f in facts)
    assert any(f["predicate"] == "duration" and f["value"] == "3 days" for f in facts)
    assert any(f["predicate"] == "age_group" and f["value"] == "older_adult" for f in facts)
    assert any(f["predicate"] == "sex" and f["value"] == "f" for f in facts)


def test_ontology_does_not_turn_non_red_flag_respiratory_symptoms_into_emergencies():
    result = TriageService().evaluate("I have a cough")
    assert result["urgency_level"] == UrgencyLevel.ROUTINE.value
    assert "RULE_RESP_001" not in result["triggered_rules"]


def test_infant_fever_rule_uses_profile_age_and_current_symptom():
    result = TriageService().evaluate("The baby has a fever", age=0.1)
    assert "RULE_INFANT_FEVER_001" in result["triggered_rules"]
    assert result["urgency_level"] == UrgencyLevel.EMERGENCY.value
