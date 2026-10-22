from app.services.ai.assessment_agent import AssessmentAgent
from app.services.clinical.ddxplus_ranker import DDXPlusRanker
from app.services.clinical.evidence_mapper import DDXPlusEvidenceMapper, duration_membership, severity_membership
from app.services.clinical.question_search import EvidenceQuestionSearch
from app.services.triage_service import TriageService


def _two_class_model():
    return {
        "classes": {"Condition A": 100, "Condition B": 100},
        "token_counts": {
            "Condition A": {"E_91": 99, "E_97": 2},
            "Condition B": {"E_91": 1, "E_97": 80},
        },
        "training_rows": 200,
        "alpha": 0.25,
    }


def test_mapper_preserves_negation_and_separates_duration_from_ranking():
    mapper = DDXPlusEvidenceMapper()
    result = mapper.map_assessment("No fever, but I have a sore throat for a few days")
    assert "E_91" not in result["evidence"]
    assert "E_91" in result["negated_codes"]
    assert "E_97" in result["evidence"]
    assert result["duration_membership"]
    assert result["duration_used_for_condition_ranking"] is False
    assert result["duration_used_for_urgency"] is False


def test_evidence_mapper_uses_symptom_ontology_for_parent_aliases():
    result = DDXPlusEvidenceMapper().map_assessment(symptoms=[{"name": "chest pressure"}])
    assert "E_53" in result["evidence"]


def test_severity_fuzzy_membership_is_bounded_and_normalized():
    mild = severity_membership("mild")
    assert all(0 <= score <= 10 and 0 <= grade <= 1 for score, grade in mild.items())
    assert abs(sum(mild.values()) - 1) < 1e-9
    assert severity_membership(11) == {10: 1.0}
    assert duration_membership("weeks") == {"ongoing": 0.35, "prolonged": 0.65}


def test_new_evidence_answer_can_change_ranked_pattern():
    model = _two_class_model()
    ranker = DDXPlusRanker(model=model, calibration={"valid": True, "temperature": 1, "min_evidence": 1, "min_top_probability": 0, "confidence_bands": {"moderate": 0, "high": 0.8}})
    mapper = DDXPlusEvidenceMapper()
    first = mapper.map_assessment("I have a sore throat")
    initial = ranker.rank(first["evidence"], min_evidence=1)
    updated = mapper.map_assessment("I have a sore throat", answers=[{"evidence_code": "E_91", "answer": "Yes"}])
    after_answer = ranker.rank(updated["evidence"], min_evidence=1)
    assert initial["ranked_conditions"][0]["condition"] == "Condition B"
    assert after_answer["ranked_conditions"][0]["condition"] == "Condition A"


def test_ranker_abstains_when_calibration_or_evidence_is_missing():
    model = _two_class_model()
    assert DDXPlusRanker(model=model, calibration={"valid": False}).rank({"E_91": 1})["abstain"]
    assert DDXPlusRanker(model=model, calibration={"valid": True, "min_evidence": 2}).rank({"E_91": 1})["reason"] == "insufficient_mapped_evidence"


def test_search_methods_return_explainable_mapper_supported_questions():
    search = EvidenceQuestionSearch(_two_class_model())
    context = search.definitions["E_91"]["context"]
    for method in ("greedy", "lookahead"):
        question = search.choose({context}, {"E_91"}, set(), method=method)
        assert question
        assert question["code"] in search.definitions
        assert question["question"]
        assert question["search_method"]


def test_agent_never_retracts_safety_emergency_for_model_result():
    agent = AssessmentAgent()
    triage = TriageService().evaluate("I have severe chest pressure")
    state = agent.update_state("I have severe chest pressure", [], [], triage, {"abstain": True}, 4)
    assert agent.select_action(state, has_candidate_question=True) == AssessmentAgent.ACTION_ESCALATE
