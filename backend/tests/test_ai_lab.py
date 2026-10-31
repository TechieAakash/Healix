import pytest
from app.ai_lab.search import SearchEngine
from app.ai_lab.logic import LogicEngine
from app.ai_lab.uncertainty import UncertaintyEngine
from app.ai_lab.games import GameEngine
from app.ai_lab.planning import GoalStackPlanner
from app.ai_lab.learning import ID3Learner

def test_a_star_search_optimal():
    res = SearchEngine.a_star_search()
    assert res.is_optimal is True
    assert res.path[0] == "Triage"
    assert res.path[-1] == "Specialist_Neurology"
    assert res.total_cost > 0
    assert len(res.steps) > 0

def test_hill_climbing_search():
    res = SearchEngine.hill_climbing()
    assert len(res.path) > 0
    assert res.start_node == "Triage"

def test_resolution_refutation():
    # Clauses: {P, Q}, {~P, Q}, {P, ~Q}, {~P, ~Q} is unsatisfiable
    clauses = [["P", "Q"], ["~P", "Q"], ["P", "~Q"], ["~P", "~Q"]]
    res = LogicEngine.resolution_refutation(clauses)
    assert res.proved is True
    assert any(s.is_empty_clause for s in res.steps)

def test_bayesian_network_inference():
    res = UncertaintyEngine.bayesian_network_query("Flu", {"Fever": True, "Fatigue": True})
    assert "True" in res.posterior_distribution
    assert res.posterior_distribution["True"] > 0.10  # Evidence increases posterior probability

def test_dempster_shafer_combination():
    res = UncertaintyEngine.dempster_shafer_combine()
    assert 0.0 <= res.conflict_k <= 1.0
    assert "Migraine" in res.belief_intervals
    assert res.belief_intervals["Migraine"]["belief"] <= res.belief_intervals["Migraine"]["plausibility"]

def test_alpha_beta_pruning():
    res = GameEngine.run_alpha_beta_demo()
    assert res.root_value == 5.0
    assert res.pruned_nodes_count > 0
    assert len(res.steps) > 0

def test_goal_stack_planning():
    res = GoalStackPlanner.run_demo_plan()
    assert res.success is True
    assert len(res.plan_actions) == 2

def test_id3_decision_tree_learning():
    res = ID3Learner.train_clinical_demo()
    assert res.root_entropy > 0
    assert len(res.feature_gains) == 3
    assert res.tree.attribute is not None
