from __future__ import annotations
from typing import List, Tuple, Set, Dict, Any
from .rules import Rule
from .facts import Fact

class ConflictResolver:
    """
    Applies production system conflict resolution strategies in strict order:
    1. Priority level (e.g. Red Flag: 1000 > Triage: 500 > Advisory: 100)
    2. Specificity (more specific condition AST leaves beat general rules)
    3. Recency (facts asserted more recently)
    4. Refractoriness (rules already fired on identical memory state are eliminated)
    """

    def __init__(self):
        self.fired_rule_signatures: Set[str] = set()

    def reset(self):
        self.fired_rule_signatures.clear()

    def generate_activation_signature(self, rule: Rule, matched_fact_ids: List[str]) -> str:
        sorted_ids = sorted(matched_fact_ids)
        return f"{rule.id}::{','.join(sorted_ids)}"

    def is_refractory(self, rule: Rule, matched_fact_ids: List[str]) -> bool:
        sig = self.generate_activation_signature(rule, matched_fact_ids)
        return sig in self.fired_rule_signatures

    def mark_fired(self, rule: Rule, matched_fact_ids: List[str]):
        sig = self.generate_activation_signature(rule, matched_fact_ids)
        self.fired_rule_signatures.add(sig)

    def resolve(
        self,
        candidate_rules: List[Tuple[Rule, List[Dict[str, Any]]]]
    ) -> List[Tuple[Rule, List[Dict[str, Any]]]]:
        """
        Takes candidate (Rule, matched_facts) pairs, filters out refractory firings,
        and sorts them by:
        (-priority, -specificity, -recency, rule.id)
        """
        eligible = []
        for rule, matched_facts in candidate_rules:
            matched_ids = [m.get("id", m.get("name", "")) for m in matched_facts]
            if not self.is_refractory(rule, matched_ids):
                # Calculate recency as max timestamp of matched facts
                max_recency = 0.0
                for m in matched_facts:
                    ts = m.get("timestamp")
                    if isinstance(ts, (int, float)):
                        max_recency = max(max_recency, ts)
                specificity = rule.get_specificity_score()
                eligible.append((rule, matched_facts, rule.priority, specificity, max_recency))

        # Sort: Highest priority first, highest specificity first, highest recency first
        eligible.sort(
            key=lambda item: (-item[2], -item[3], -item[4], item[0].id)
        )

        return [(item[0], item[1]) for item in eligible]

