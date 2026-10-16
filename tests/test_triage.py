from app.services.triage_service import TriageService
from app.utils.constants import UrgencyLevel


def test_triage_routine_scenario():
    service = TriageService()
    result = service.evaluate(
        description="Mild headache after working on computer",
        symptoms=[{"name": "Headache", "severity": 4}],
    )
    assert result["urgency_level"] == UrgencyLevel.ROUTINE.value
    assert result["requires_professional_attention"] is False
    assert len(result["triggered_rules"]) == 0


def test_triage_emergency_cardiovascular_scenario():
    service = TriageService()
    result = service.evaluate(
        description="I have severe chest pain radiating to arm and jaw",
        symptoms=[{"name": "Chest Pain", "severity": 8}],
    )
    assert result["urgency_level"] == UrgencyLevel.EMERGENCY.value
    assert result["requires_professional_attention"] is True
    assert "RULE_CARDIO_001" in result["triggered_rules"]
    assert "emergency" in result["message"].lower()


def test_triage_emergency_neurological_scenario():
    service = TriageService()
    result = service.evaluate(
        description="Sudden onset worst headache of my life with slurred speech",
        symptoms=[{"name": "Thunderclap Headache", "severity": 10}],
    )
    assert result["urgency_level"] == UrgencyLevel.EMERGENCY.value
    assert "RULE_NEURO_001" in result["triggered_rules"]


def test_triage_urgent_severity_threshold():
    service = TriageService()
    result = service.evaluate(
        description="Severe knee pain after sports",
        symptoms=[{"name": "Knee Pain", "severity": 9}], # >= 9 triggers urgent threshold
    )
    assert result["urgency_level"] == UrgencyLevel.URGENT.value
    assert "RULE_SEV_001" in result["triggered_rules"]
