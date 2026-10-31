from __future__ import annotations
from enum import Enum
from typing import Any, List, Optional, Union, Dict
from pydantic import BaseModel, Field
from .facts import FactValue

class RuleCategory(str, Enum):
    EMERGENCY_RED_FLAG = "EMERGENCY_RED_FLAG"
    CLINICAL_TRIAGE = "CLINICAL_TRIAGE"
    SYMPTOM_ASSOCIATION = "SYMPTOM_ASSOCIATION"
    SELF_CARE_GUIDANCE = "SELF_CARE_GUIDANCE"

class Operator(str, Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    IN_SET = "IN_SET"
    EXISTS = "EXISTS"

class SimpleCondition(BaseModel):
    fact_name: str
    operator: Operator = Operator.EQUALS
    target_value: Any = FactValue.TRUE

    def get_referenced_facts(self) -> List[str]:
        return [self.fact_name]

class CompoundCondition(BaseModel):
    logical_operator: str = "AND"  # "AND" | "OR" | "NOT"
    conditions: List[Union[SimpleCondition, CompoundCondition]]

    def get_referenced_facts(self) -> List[str]:
        facts = []
        for c in self.conditions:
            facts.extend(c.get_referenced_facts())
        return list(set(facts))

class RecommendationTier(str, Enum):
    EMERGENCY = "EMERGENCY"
    URGENT_EVALUATION = "URGENT_EVALUATION"
    CONSULT_PHYSICIAN = "CONSULT_PHYSICIAN"
    SELF_MONITOR = "SELF_MONITOR"
    ROUTINE_PREVENTIVE = "ROUTINE_PREVENTIVE"

class Conclusion(BaseModel):
    id: str
    fact_name: str
    asserted_value: FactValue = FactValue.TRUE
    confidence: float = 1.0
    category: str = "OBSERVATION"
    summary: str
    detailed_explanation: str
    recommendation_tier: RecommendationTier = RecommendationTier.CONSULT_PHYSICIAN
    actionable_steps: List[str] = Field(default_factory=list)

class RuleTestCase(BaseModel):
    case_name: str
    input_facts: Dict[str, Any]
    expected_to_fire: bool
    expected_conclusions: List[str] = Field(default_factory=list)

class Rule(BaseModel):
    id: str                              # e.g., "RULE_MIGRAINE_042"
    name: str
    description: str
    conditions: Union[CompoundCondition, SimpleCondition]
    conclusions: List[Conclusion]
    priority: int = 500                  # 1000 = Red Flag, 500 = Triage, 100 = General
    category: RuleCategory = RuleCategory.CLINICAL_TRIAGE
    version: str = "1.0.0"
    provenance: str                      # Clinical reference or textbook citation
    review_status: str = "APPROVED"      # DRAFT, APPROVED, DEPRECATED
    is_active: bool = True
    test_cases: List[RuleTestCase] = Field(default_factory=list)

    def get_all_required_facts(self) -> List[str]:
        return self.conditions.get_referenced_facts()

    def get_specificity_score(self) -> int:
        """Specificity score is the count of individual condition leaves in AST."""
        if isinstance(self.conditions, SimpleCondition):
            return 1
        return len(self.get_all_required_facts())

