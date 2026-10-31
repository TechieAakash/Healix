import pytest
from app.engine.facts import Fact, FactValue
from app.engine.rules import (
    Rule, RuleCategory, SimpleCondition, CompoundCondition, Operator,
    Conclusion, RecommendationTier
)
from app.engine.matching import match_rule
from app.engine.unification import Unifier, parse_term
from app.engine.conflict_resolution import ConflictResolver
from app.engine.forward_chaining import ForwardChainingEngine
from app.engine.backward_chaining import BackwardChainingEngine
from app.engine.explainability import ExplainabilityEngine
from app.engine.knowledge_base.rules_data import get_clinical_knowledge_base, KB_VERSION

def test_fact_5_valued_logic():
    f_true = Fact(name="test.true", value=FactValue.TRUE)
    f_false = Fact(name="test.false", value=FactValue.FALSE)
    f_unk = Fact(name="test.unk", value=FactValue.UNKNOWN)
    f_na = Fact(name="test.na", value=FactValue.NOT_APPLICABLE)

    assert f_true.is_definitely_true()
    assert not f_true.is_definitely_false()
    assert f_false.is_definitely_false()
    assert f_unk.is_missing()
    assert not f_na.is_known()

def test_unification_algorithm_with_occurs_check():
    unifier = Unifier()

    # 1. Successful unification: P(?x, Bob) and P(Alice, ?y) -> {?x: Alice, ?y: Bob}
    res1 = unifier.unify_strings("P(?x, Bob)", "P(Alice, ?y)")
    assert res1.success is True
    assert res1.mgu.get("?x") == "Alice"
    assert res1.mgu.get("?y") == "Bob"

    # 2. Occurs-check failure: ?x and f(?x) -> Failure (infinite term)
    res2 = unifier.unify_strings("?x", "f(?x)")
    assert res2.success is False
    assert "infinite term" in res2.failure_reason.lower() or "occurs" in res2.failure_reason.lower()

    # 3. Predicate mismatch: AllergicTo(?x, Penicillin) and Prescribed(?x, Penicillin) -> Clash
    res3 = unifier.unify_strings("AllergicTo(?x, Penicillin)", "Prescribed(?x, Penicillin)")
    assert res3.success is False

def test_conflict_resolution_priority_and_specificity():
    resolver = ConflictResolver()

    # Rule A: General triage (priority 500, 1 condition)
    rule_a = Rule(
        id="RULE_A",
        name="General Rule",
        description="General",
        priority=500,
        provenance="Test Citation A",
        conditions=SimpleCondition(fact_name="symptom.headache", operator=Operator.EQUALS, target_value=FactValue.TRUE),
        conclusions=[]
    )

    # Rule B: Specific triage (priority 500, 2 conditions)
    rule_b = Rule(
        id="RULE_B",
        name="Specific Rule",
        description="Specific",
        priority=500,
        provenance="Test Citation B",
        conditions=CompoundCondition(
            logical_operator="AND",
            conditions=[
                SimpleCondition(fact_name="symptom.headache", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                SimpleCondition(fact_name="symptom.photophobia", operator=Operator.EQUALS, target_value=FactValue.TRUE)
            ]
        ),
        conclusions=[]
    )

    # Rule C: Red Flag (priority 1000)
    rule_c = Rule(
        id="RULE_C",
        name="Emergency Rule",
        description="Emergency",
        priority=1000,
        provenance="Test Citation C",
        category=RuleCategory.EMERGENCY_RED_FLAG,
        conditions=SimpleCondition(fact_name="symptom.thunderclap", operator=Operator.EQUALS, target_value=FactValue.TRUE),
        conclusions=[]
    )

    candidates = [
        (rule_a, [{"name": "symptom.headache"}]),
        (rule_b, [{"name": "symptom.headache"}, {"name": "symptom.photophobia"}]),
        (rule_c, [{"name": "symptom.thunderclap"}])
    ]

    resolved = resolver.resolve(candidates)
    order_ids = [r[0].id for r in resolved]

    # Rule C (priority 1000) must be first.
    # Rule B (priority 500, specificity 2) must precede Rule A (priority 500, specificity 1).
    assert order_ids == ["RULE_C", "RULE_B", "RULE_A"]

def test_forward_chaining_migraine_scenario():
    kb = get_clinical_knowledge_base()
    engine = ForwardChainingEngine(rules=kb)

    # Patient with unilateral throbbing headache and photophobia, no red flags
    facts = [
        Fact(name="symptom.headache.present", value=FactValue.TRUE),
        Fact(name="symptom.headache.throbbing", value=FactValue.TRUE),
        Fact(name="symptom.photophobia", value=FactValue.TRUE),
        Fact(name="symptom.headache.onset_thunderclap", value=FactValue.FALSE),
        Fact(name="symptom.neck_stiffness", value=FactValue.FALSE),
        Fact(name="symptom.fever", value=FactValue.FALSE)
    ]

    output = engine.run(facts)

    assert not output.emergency_flagged
    assert len(output.fired_rules) > 0

    fired_rule_ids = [f.rule_id for f in output.fired_rules]
    assert "RULE_MIGRAINE_042" in fired_rule_ids

    conclusions = output.final_conclusions
    assert any("Migraine Pattern" in c.summary for c in conclusions)

def test_forward_chaining_emergency_red_flag_scenario():
    kb = get_clinical_knowledge_base()
    engine = ForwardChainingEngine(rules=kb)

    # Patient reports sudden excruciating thunderclap headache
    facts = [
        Fact(name="symptom.headache.present", value=FactValue.TRUE),
        Fact(name="symptom.headache.onset_thunderclap", value=FactValue.TRUE)
    ]

    output = engine.run(facts)

    assert output.emergency_flagged is True
    fired_rule_ids = [f.rule_id for f in output.fired_rules]
    assert "RULE_EMERGENCY_THUNDERCLAP" in fired_rule_ids
    assert any(c.recommendation_tier == RecommendationTier.EMERGENCY for c in output.final_conclusions)

def test_backward_chaining_deduces_missing_facts():
    kb = get_clinical_knowledge_base()
    b_engine = BackwardChainingEngine(rules=kb)

    # Memory only knows headache is present and throbbing
    working_memory = {
        "symptom.headache.present": Fact(name="symptom.headache.present", value=FactValue.TRUE),
        "symptom.headache.throbbing": Fact(name="symptom.headache.throbbing", value=FactValue.TRUE)
    }

    # Query if migraine pattern is proven
    res = b_engine.query("observation.triage.migraine_pattern", FactValue.TRUE, working_memory)

    assert not res.is_proven
    # It must correctly deduce that photophobia/nausea or negative red flags are missing
    assert len(res.all_missing_facts_needed) > 0
    assert any("photophobia" in m or "thunderclap" in m or "neck_stiffness" in m for m in res.all_missing_facts_needed)

def test_explainability_trace_and_graph_generation():
    kb = get_clinical_knowledge_base()
    engine = ForwardChainingEngine(rules=kb)

    facts = [
        Fact(name="symptom.headache.present", value=FactValue.TRUE),
        Fact(name="symptom.headache.throbbing", value=FactValue.TRUE),
        Fact(name="symptom.photophobia", value=FactValue.TRUE),
        Fact(name="symptom.headache.onset_thunderclap", value=FactValue.FALSE),
        Fact(name="symptom.neck_stiffness", value=FactValue.FALSE)
    ]

    output = engine.run(facts)

    trace = ExplainabilityEngine.build_graph_and_trace(
        assessment_id="test_assessment_123",
        kb_version=KB_VERSION,
        initial_facts=facts,
        working_memory=output.working_memory,
        fired_rules=output.fired_rules,
        skipped_rules=output.skipped_rules,
        final_conclusions=output.final_conclusions,
        emergency_flagged=output.emergency_flagged,
        iterations_run=output.iterations_run,
        execution_time_ms=output.execution_time_ms
    )

    assert trace.assessment_id == "test_assessment_123"
    assert len(trace.graph_payload.nodes) > 0
    assert len(trace.graph_payload.edges) > 0
    # Verify node types exist
    types = {n.type for n in trace.graph_payload.nodes}
    assert "factNode" in types
    assert "ruleNode" in types
    assert "conclusionNode" in types
