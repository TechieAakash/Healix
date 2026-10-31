from __future__ import annotations
from typing import Dict, List, Tuple, Any, Optional
from pydantic import BaseModel, Field
from .facts import Fact, FactValue
from .rules import SimpleCondition, CompoundCondition, Operator, Rule

class ConditionEvaluationResult(BaseModel):
    value: FactValue
    is_satisfied: bool
    matched_facts: List[Dict[str, Any]] = Field(default_factory=list)
    unsatisfied_conditions: List[str] = Field(default_factory=list)
    missing_facts: List[str] = Field(default_factory=list)

def evaluate_simple_condition(condition: SimpleCondition, working_memory: Dict[str, Fact]) -> ConditionEvaluationResult:
    # Normalize FactValue target comparison
    target = condition.target_value
    if isinstance(target, str) and target in FactValue.__members__:
        target = FactValue[target]

    fact = working_memory.get(condition.fact_name)
    if not fact:
        # Negation-as-failure / absence of red flag:
        # If the condition requires that a fact is NOT TRUE (NOT_EQUALS TRUE),
        # an unasserted fact is indeed NOT TRUE.
        if condition.operator == Operator.NOT_EQUALS and target == FactValue.TRUE:
            return ConditionEvaluationResult(
                value=FactValue.TRUE,
                is_satisfied=True,
                matched_facts=[]
            )
        return ConditionEvaluationResult(
            value=FactValue.NOT_ASKED,
            is_satisfied=False,
            unsatisfied_conditions=[f"Fact '{condition.fact_name}' has not been asked/recorded"],
            missing_facts=[condition.fact_name]
        )

    if fact.value in (FactValue.UNKNOWN, FactValue.NOT_ASKED):
        if condition.operator == Operator.NOT_EQUALS and target == FactValue.TRUE:
            return ConditionEvaluationResult(
                value=FactValue.TRUE,
                is_satisfied=True,
                matched_facts=[]
            )
        return ConditionEvaluationResult(
            value=fact.value,
            is_satisfied=False,
            unsatisfied_conditions=[f"Fact '{condition.fact_name}' is currently {fact.value.value}"],
            missing_facts=[condition.fact_name]
        )

    if fact.value == FactValue.NOT_APPLICABLE:
        return ConditionEvaluationResult(
            value=FactValue.NOT_APPLICABLE,
            is_satisfied=False,
            unsatisfied_conditions=[f"Fact '{condition.fact_name}' is NOT_APPLICABLE"]
        )

    # Compare values
    actual = fact.raw_value if fact.raw_value is not None else fact.value

    satisfied = False
    op = condition.operator

    try:
        if op == Operator.EQUALS:
            satisfied = (actual == target) or (fact.value == target)
        elif op == Operator.NOT_EQUALS:
            satisfied = (actual != target) and (fact.value != target)
        elif op == Operator.GREATER_THAN:
            satisfied = float(actual) > float(target)
        elif op == Operator.LESS_THAN:
            satisfied = float(actual) < float(target)
        elif op == Operator.GREATER_EQUAL:
            satisfied = float(actual) >= float(target)
        elif op == Operator.LESS_EQUAL:
            satisfied = float(actual) <= float(target)
        elif op == Operator.IN_SET:
            satisfied = actual in target
        elif op == Operator.EXISTS:
            satisfied = fact.is_known()
    except (TypeError, ValueError):
        satisfied = False

    if satisfied:
        return ConditionEvaluationResult(
            value=FactValue.TRUE,
            is_satisfied=True,
            matched_facts=[fact.model_dump(mode="json")]
        )
    else:
        return ConditionEvaluationResult(
            value=FactValue.FALSE,
            is_satisfied=False,
            unsatisfied_conditions=[
                f"Expected {condition.fact_name} {op.value} {target}, but got {actual}"
            ]
        )

def evaluate_compound_condition(condition: CompoundCondition, working_memory: Dict[str, Fact]) -> ConditionEvaluationResult:
    results = [
        evaluate_condition(c, working_memory)
        for c in condition.conditions
    ]

    op = condition.logical_operator.upper()
    all_matched = []
    all_unsatisfied = []
    all_missing = []

    for r in results:
        all_matched.extend(r.matched_facts)
        all_unsatisfied.extend(r.unsatisfied_conditions)
        all_missing.extend(r.missing_facts)

    if op == "AND":
        # If any is definitely FALSE -> overall is FALSE
        if any(r.value == FactValue.FALSE for r in results):
            return ConditionEvaluationResult(
                value=FactValue.FALSE,
                is_satisfied=False,
                unsatisfied_conditions=all_unsatisfied,
                missing_facts=all_missing
            )
        # If all are TRUE -> overall is TRUE
        if all(r.value == FactValue.TRUE for r in results):
            return ConditionEvaluationResult(
                value=FactValue.TRUE,
                is_satisfied=True,
                matched_facts=all_matched
            )
        # Otherwise unknown / missing
        return ConditionEvaluationResult(
            value=FactValue.UNKNOWN,
            is_satisfied=False,
            unsatisfied_conditions=all_unsatisfied,
            missing_facts=all_missing
        )

    elif op == "OR":
        # If any is TRUE -> overall is TRUE
        if any(r.value == FactValue.TRUE for r in results):
            return ConditionEvaluationResult(
                value=FactValue.TRUE,
                is_satisfied=True,
                matched_facts=[m for r in results if r.value == FactValue.TRUE for m in r.matched_facts]
            )
        # If all are definitely FALSE -> overall is FALSE
        if all(r.value == FactValue.FALSE for r in results):
            return ConditionEvaluationResult(
                value=FactValue.FALSE,
                is_satisfied=False,
                unsatisfied_conditions=all_unsatisfied,
                missing_facts=all_missing
            )
        return ConditionEvaluationResult(
            value=FactValue.UNKNOWN,
            is_satisfied=False,
            unsatisfied_conditions=all_unsatisfied,
            missing_facts=all_missing
        )

    elif op == "NOT":
        if not results:
            return ConditionEvaluationResult(value=FactValue.UNKNOWN, is_satisfied=False)
        first = results[0]
        if first.value == FactValue.TRUE:
            return ConditionEvaluationResult(
                value=FactValue.FALSE,
                is_satisfied=False,
                unsatisfied_conditions=["NOT condition failed: underlying condition was TRUE"]
            )
        elif first.value == FactValue.FALSE:
            return ConditionEvaluationResult(
                value=FactValue.TRUE,
                is_satisfied=True,
                matched_facts=first.matched_facts
            )
        else:
            return ConditionEvaluationResult(
                value=FactValue.UNKNOWN,
                is_satisfied=False,
                missing_facts=first.missing_facts
            )

    return ConditionEvaluationResult(value=FactValue.UNKNOWN, is_satisfied=False)

def evaluate_condition(condition: Any, working_memory: Dict[str, Fact]) -> ConditionEvaluationResult:
    if isinstance(condition, SimpleCondition):
        return evaluate_simple_condition(condition, working_memory)
    elif isinstance(condition, CompoundCondition):
        return evaluate_compound_condition(condition, working_memory)
    raise TypeError(f"Unsupported condition type: {type(condition)}")

def match_rule(rule: Rule, working_memory: Dict[str, Fact]) -> ConditionEvaluationResult:
    if not rule.is_active:
        return ConditionEvaluationResult(
            value=FactValue.FALSE,
            is_satisfied=False,
            unsatisfied_conditions=[f"Rule '{rule.id}' is deactivated"]
        )
    return evaluate_condition(rule.conditions, working_memory)

