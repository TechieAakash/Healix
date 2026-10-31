from .facts import Fact, FactValue
from .rules import (
    Rule, RuleCategory, Operator, SimpleCondition, CompoundCondition,
    Conclusion, RecommendationTier, RuleTestCase
)
from .matching import match_rule, evaluate_condition, ConditionEvaluationResult
from .conflict_resolution import ConflictResolver
from .forward_chaining import ForwardChainingEngine, ForwardChainingOutput
from .backward_chaining import BackwardChainingEngine, BackwardChainingResult
from .unification import Unifier, Term, parse_term, UnificationResult
from .explainability import ExplainabilityEngine, InferenceTrace, GraphPayload
from .knowledge_base.rules_data import get_clinical_knowledge_base, KB_VERSION

__all__ = [
    "Fact",
    "FactValue",
    "Rule",
    "RuleCategory",
    "Operator",
    "SimpleCondition",
    "CompoundCondition",
    "Conclusion",
    "RecommendationTier",
    "RuleTestCase",
    "match_rule",
    "evaluate_condition",
    "ConditionEvaluationResult",
    "ConflictResolver",
    "ForwardChainingEngine",
    "ForwardChainingOutput",
    "BackwardChainingEngine",
    "BackwardChainingResult",
    "Unifier",
    "Term",
    "parse_term",
    "UnificationResult",
    "ExplainabilityEngine",
    "InferenceTrace",
    "GraphPayload",
    "get_clinical_knowledge_base",
    "KB_VERSION",
]

