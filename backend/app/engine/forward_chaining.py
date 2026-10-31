from __future__ import annotations
import time
from typing import List, Dict, Any, Tuple, Optional
from pydantic import BaseModel, Field
from .facts import Fact, FactValue
from .rules import Rule, RuleCategory, Conclusion
from .matching import match_rule
from .conflict_resolution import ConflictResolver

class RuleFiringRecord(BaseModel):
    iteration: int
    rule_id: str
    rule_name: str
    priority: int
    category: str
    matched_facts: List[Dict[str, Any]]
    asserted_conclusions: List[Dict[str, Any]]
    execution_duration_ms: float

class RuleSkippedRecord(BaseModel):
    rule_id: str
    rule_name: str
    priority: int
    category: str
    unsatisfied_conditions: List[str]
    missing_facts: List[str]

class ForwardChainingOutput(BaseModel):
    working_memory: Dict[str, Fact]
    fired_rules: List[RuleFiringRecord]
    skipped_rules: List[RuleSkippedRecord]
    final_conclusions: List[Conclusion]
    emergency_flagged: bool = False
    iterations_run: int
    execution_time_ms: float

class ForwardChainingEngine:
    def __init__(self, rules: List[Rule], max_iterations: int = 25):
        self.rules = rules
        self.max_iterations = max_iterations
        self.conflict_resolver = ConflictResolver()

    def run(self, initial_facts: List[Fact]) -> ForwardChainingOutput:
        start_time = time.perf_counter()
        self.conflict_resolver.reset()

        working_memory: Dict[str, Fact] = {f.name: f for f in initial_facts}
        fired_records: List[RuleFiringRecord] = []
        skipped_records_map: Dict[str, RuleSkippedRecord] = {}
        final_conclusions: List[Conclusion] = []
        emergency_flagged = False

        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            candidates: List[Tuple[Rule, List[Dict[str, Any]]]] = []

            for rule in self.rules:
                eval_res = match_rule(rule, working_memory)
                if eval_res.is_satisfied:
                    candidates.append((rule, eval_res.matched_facts))
                    # Remove from skipped if it previously was skipped
                    skipped_records_map.pop(rule.id, None)
                else:
                    if rule.id not in [f.rule_id for f in fired_records]:
                        skipped_records_map[rule.id] = RuleSkippedRecord(
                            rule_id=rule.id,
                            rule_name=rule.name,
                            priority=rule.priority,
                            category=rule.category.value,
                            unsatisfied_conditions=eval_res.unsatisfied_conditions,
                            missing_facts=eval_res.missing_facts
                        )

            if not candidates:
                # Fixed-point reached: no rules satisfied
                break

            # Resolve conflict among satisfied rules
            resolved_candidates = self.conflict_resolver.resolve(candidates)
            if not resolved_candidates:
                # All satisfied rules are refractory
                break

            # Fire the winning rule
            winning_rule, winning_matched_facts = resolved_candidates[0]
            matched_fact_ids = [m.get("id", m.get("name", "")) for m in winning_matched_facts]
            self.conflict_resolver.mark_fired(winning_rule, matched_fact_ids)

            fire_start = time.perf_counter()
            asserted_conclusions_payload = []

            for conclusion in winning_rule.conclusions:
                final_conclusions.append(conclusion)
                asserted_conclusions_payload.append(conclusion.model_dump(mode="json"))

                # Add new fact derived by conclusion into working memory
                derived_fact = Fact(
                    name=conclusion.fact_name,
                    value=conclusion.asserted_value,
                    certainty=conclusion.confidence,
                    data_type="boolean",
                    source="DERIVED",
                    metadata={
                        "rule_id": winning_rule.id,
                        "iteration": iteration,
                        "recommendation_tier": conclusion.recommendation_tier.value
                    }
                )
                working_memory[derived_fact.name] = derived_fact

            if winning_rule.category == RuleCategory.EMERGENCY_RED_FLAG:
                emergency_flagged = True

            fire_duration = (time.perf_counter() - fire_start) * 1000.0

            fired_records.append(
                RuleFiringRecord(
                    iteration=iteration,
                    rule_id=winning_rule.id,
                    rule_name=winning_rule.name,
                    priority=winning_rule.priority,
                    category=winning_rule.category.value,
                    matched_facts=winning_matched_facts,
                    asserted_conclusions=asserted_conclusions_payload,
                    execution_duration_ms=round(fire_duration, 3)
                )
            )

            # If emergency red flag triggered, we can continue or halt based on safety
            # Healix lets red-flag rule fire first and continue to collect context,
            # while emergency_flagged will trigger high-priority UI alert.

        total_time = (time.perf_counter() - start_time) * 1000.0

        return ForwardChainingOutput(
            working_memory=working_memory,
            fired_rules=fired_records,
            skipped_rules=list(skipped_records_map.values()),
            final_conclusions=final_conclusions,
            emergency_flagged=emergency_flagged,
            iterations_run=iteration,
            execution_time_ms=round(total_time, 2)
        )

