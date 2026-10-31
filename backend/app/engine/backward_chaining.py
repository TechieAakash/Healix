from __future__ import annotations
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
from .facts import Fact, FactValue
from .rules import Rule, SimpleCondition, CompoundCondition

class GoalEvaluationNode(BaseModel):
    goal_fact: str
    target_value: Any
    status: str  # "PROVEN" | "DISPROVEN" | "UNKNOWN" | "SUBGOAL_EXPLORATION"
    rule_id: Optional[str] = None
    subgoals: List[GoalEvaluationNode] = Field(default_factory=list)
    missing_facts_required: List[str] = Field(default_factory=list)
    explanation: str

class BackwardChainingResult(BaseModel):
    goal: str
    is_proven: bool
    proof_tree: GoalEvaluationNode
    all_missing_facts_needed: List[str]
    rules_consulted: List[str]

class BackwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def evaluate_goal(
        self,
        target_fact_name: str,
        target_value: Any,
        working_memory: Dict[str, Fact],
        visited_goals: Optional[Set[str]] = None
    ) -> GoalEvaluationNode:
        if visited_goals is None:
            visited_goals = set()

        goal_signature = f"{target_fact_name}=={target_value}"
        if goal_signature in visited_goals:
            return GoalEvaluationNode(
                goal_fact=target_fact_name,
                target_value=target_value,
                status="UNKNOWN",
                explanation=f"Cycle detected while proving {goal_signature}"
            )
        visited_goals.add(goal_signature)

        # 1. Check if fact is directly present in working memory
        if target_fact_name in working_memory:
            fact = working_memory[target_fact_name]
            if fact.value == target_value or (fact.raw_value is not None and fact.raw_value == target_value):
                return GoalEvaluationNode(
                    goal_fact=target_fact_name,
                    target_value=target_value,
                    status="PROVEN",
                    explanation=f"Fact '{target_fact_name}' is known directly as {fact.value.value}"
                )
            elif fact.value in (FactValue.FALSE, FactValue.NOT_APPLICABLE):
                return GoalEvaluationNode(
                    goal_fact=target_fact_name,
                    target_value=target_value,
                    status="DISPROVEN",
                    explanation=f"Fact '{target_fact_name}' is known to be {fact.value.value}, which contradicts {target_value}"
                )

        # 2. Find rules that can conclude this target fact
        matching_rules = []
        for rule in self.rules:
            for conclusion in rule.conclusions:
                if conclusion.fact_name == target_fact_name and conclusion.asserted_value == target_value:
                    matching_rules.append(rule)

        if not matching_rules:
            # Cannot be concluded by any rule and not in memory -> missing fact
            return GoalEvaluationNode(
                goal_fact=target_fact_name,
                target_value=target_value,
                status="UNKNOWN",
                missing_facts_required=[target_fact_name],
                explanation=f"No rules conclude '{target_fact_name}'. Need user input."
            )

        # Try to prove via at least one rule
        for rule in matching_rules:
            subgoals: List[GoalEvaluationNode] = []
            all_subgoals_proven = True
            missing_for_rule: List[str] = []

            # Deconstruct conditions into subgoals
            required_facts = rule.get_all_required_facts()
            for req_fact in required_facts:
                sub_res = self.evaluate_goal(
                    target_fact_name=req_fact,
                    target_value=FactValue.TRUE,
                    working_memory=working_memory,
                    visited_goals=set(visited_goals)
                )
                subgoals.append(sub_res)
                if sub_res.status != "PROVEN":
                    all_subgoals_proven = False
                missing_for_rule.extend(sub_res.missing_facts_required)

            if all_subgoals_proven:
                return GoalEvaluationNode(
                    goal_fact=target_fact_name,
                    target_value=target_value,
                    status="PROVEN",
                    rule_id=rule.id,
                    subgoals=subgoals,
                    explanation=f"Proven via rule '{rule.name}' ({rule.id})"
                )
            else:
                return GoalEvaluationNode(
                    goal_fact=target_fact_name,
                    target_value=target_value,
                    status="UNKNOWN",
                    rule_id=rule.id,
                    subgoals=subgoals,
                    missing_facts_required=list(set(missing_for_rule)),
                    explanation=f"Could not prove rule '{rule.name}' due to missing preconditions"
                )

        return GoalEvaluationNode(
            goal_fact=target_fact_name,
            target_value=target_value,
            status="UNKNOWN",
            explanation=f"Unable to establish hypothesis {target_fact_name}"
        )

    def query(self, goal_fact_name: str, target_value: Any, working_memory: Dict[str, Fact]) -> BackwardChainingResult:
        proof_tree = self.evaluate_goal(goal_fact_name, target_value, working_memory)
        all_missing = list(set(proof_tree.missing_facts_required))
        
        # Collect rules consulted
        def collect_rules(node: GoalEvaluationNode) -> List[str]:
            r = []
            if node.rule_id:
                r.append(node.rule_id)
            for s in node.subgoals:
                r.extend(collect_rules(s))
            return list(set(r))

        return BackwardChainingResult(
            goal=f"{goal_fact_name} == {target_value}",
            is_proven=(proof_tree.status == "PROVEN"),
            proof_tree=proof_tree,
            all_missing_facts_needed=all_missing,
            rules_consulted=collect_rules(proof_tree)
        )

