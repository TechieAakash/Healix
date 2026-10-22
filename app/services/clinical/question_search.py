"""Offline search over evidence questions that the mapper can actually consume.

Both search policies use the same Bernoulli Naive Bayes state: known evidence
codes are facts and each candidate is an ask operator with Yes/No branches.
The best-first policy uses a bounded depth-two lookahead; its objective is
expected leaf entropy plus one hundredth of the expected question count.
"""

from __future__ import annotations

import heapq
import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from app.services.clinical.evidence_mapper import evidence_definitions


MODEL_PATH = Path(__file__).resolve().parents[3] / "data" / "models" / "ddxplus_nb.json"


@lru_cache(maxsize=1)
def load_model() -> Dict[str, Any]:
    with MODEL_PATH.open(encoding="utf-8") as source:
        return json.load(source)


def entropy(probabilities: Iterable[float]) -> float:
    return -sum(p * math.log(max(p, 1e-15), 2) for p in probabilities if p > 0)


class EvidenceQuestionSearch:
    """Compare one-step information-gain hill climbing with two-step lookahead."""

    def __init__(self, model: Optional[Dict[str, Any]] = None, evidence_map: Optional[Dict[str, Dict[str, Any]]] = None):
        self.model = model or load_model()
        self.definitions = evidence_map or evidence_definitions()
        self.labels = list(self.model["classes"])
        self.priors = {label: self.model["classes"][label] / self.model["training_rows"] for label in self.labels}
        self.alpha = float(self.model.get("alpha", 0.25))
        self._posterior_cache: Dict[Tuple[Tuple[str, ...], Tuple[str, ...]], Dict[str, float]] = {}

    def _p_yes(self, code: str, label: str) -> float:
        count = self.model["token_counts"][label].get(code, 0)
        class_count = self.model["classes"][label]
        return min(1 - 1e-9, max(1e-9, (count + self.alpha) / (class_count + 2 * self.alpha)))

    def posterior(self, known_yes: Set[str], known_no: Set[str]) -> Dict[str, float]:
        key = (tuple(sorted(known_yes)), tuple(sorted(known_no)))
        cached = self._posterior_cache.get(key)
        if cached is not None:
            return cached
        logits = {}
        for label in self.labels:
            score = math.log(self.priors[label])
            for code in known_yes:
                score += math.log(self._p_yes(code, label))
            for code in known_no:
                score += math.log(1 - self._p_yes(code, label))
            logits[label] = score
        peak = max(logits.values())
        weights = {label: math.exp(value - peak) for label, value in logits.items()}
        total = sum(weights.values())
        result = {label: value / total for label, value in weights.items()}
        self._posterior_cache[key] = result
        return result

    def _answer_prob(self, code: str, posterior: Dict[str, float]) -> float:
        return sum(posterior[label] * self._p_yes(code, label) for label in self.labels)

    def _expected_entropy(self, code: str, yes: Set[str], no: Set[str]) -> float:
        posterior = self.posterior(yes, no)
        p_yes = self._answer_prob(code, posterior)
        yes_post = self.posterior(yes | {code}, no)
        no_post = self.posterior(yes, no | {code})
        return p_yes * entropy(yes_post.values()) + (1 - p_yes) * entropy(no_post.values())

    def candidates(self, contexts: Iterable[str], known: Set[str], asked: Set[str]) -> List[Dict[str, Any]]:
        contexts = set(contexts)
        result = []
        for code, definition in self.definitions.items():
            if not definition.get("askable") or definition.get("data_type") != "B":
                continue
            if code in known or code in asked or definition.get("is_antecedent"):
                continue
            if contexts and definition.get("context") not in contexts:
                continue
            result.append({"code": code, **definition})
        return result

    def greedy(self, contexts: Iterable[str], known_yes: Set[str], known_no: Set[str], asked: Optional[Set[str]] = None) -> Optional[Dict[str, Any]]:
        asked = asked or set()
        candidates = self.candidates(contexts, known_yes | known_no, asked)
        if not candidates:
            return None
        current_entropy = entropy(self.posterior(known_yes, known_no).values())
        ranked = []
        for candidate in candidates:
            gain = current_entropy - self._expected_entropy(candidate["code"], known_yes, known_no)
            ranked.append((gain, candidate["code"], candidate))
        gain, _, chosen = max(ranked, key=lambda item: (item[0], item[1]))
        return {**chosen, "expected_information_gain_bits": max(0.0, gain), "search_method": "greedy_information_gain"}

    def lookahead(self, contexts: Iterable[str], known_yes: Set[str], known_no: Set[str], asked: Optional[Set[str]] = None, depth: int = 2) -> Optional[Dict[str, Any]]:
        """Bounded best-first search minimizing question cost plus expected entropy."""
        asked = asked or set()
        candidates = self.candidates(contexts, known_yes | known_no, asked)
        if not candidates:
            return None
        base_entropy = entropy(self.posterior(known_yes, known_no).values())
        frontier = []
        confidence_threshold = 0.70
        for first in candidates:
            code = first["code"]
            p_yes = self._answer_prob(code, self.posterior(known_yes, known_no))
            branches = ((p_yes, known_yes | {code}, known_no), (1 - p_yes, known_yes, known_no | {code}))
            expected_leaf_entropy = 0.0
            expected_question_count = 1.0
            for probability, yes_state, no_state in branches:
                state_entropy = entropy(self.posterior(yes_state, no_state).values())
                state_confidence = max(self.posterior(yes_state, no_state).values())
                if state_confidence >= confidence_threshold:
                    expected_leaf_entropy += probability * state_entropy
                    continue
                if depth <= 1:
                    expected_leaf_entropy += probability * state_entropy
                    continue
                second_candidates = self.candidates(contexts, yes_state | no_state, asked | {code})
                if not second_candidates:
                    expected_leaf_entropy += probability * state_entropy
                    continue
                expected_question_count += probability
                # Best-first leaf heuristic: choose the second question with the
                # lowest expected posterior entropy, deterministic on evidence code.
                leaves = [(self._expected_entropy(q["code"], yes_state, no_state), q["code"]) for q in second_candidates]
                expected_leaf_entropy += probability * min(leaves)[0]
            # Every extra question has unit cost; entropy is the heuristic term.
            objective = expected_leaf_entropy + 0.01 * expected_question_count
            heapq.heappush(frontier, (objective, code, first, expected_leaf_entropy, expected_question_count))
        _, _, chosen, expected_entropy, question_cost = heapq.heappop(frontier)
        return {
            **chosen,
            "expected_information_gain_bits": max(0.0, base_entropy - expected_entropy),
            "expected_remaining_entropy_bits": expected_entropy,
            "expected_questions": question_cost,
            "search_method": "best_first_two_step",
        }

    def choose(self, contexts: Iterable[str], known_yes: Set[str], known_no: Set[str], asked: Optional[Set[str]] = None, method: str = "lookahead") -> Optional[Dict[str, Any]]:
        if method == "greedy":
            return self.greedy(contexts, known_yes, known_no, asked)
        return self.lookahead(contexts, known_yes, known_no, asked)
