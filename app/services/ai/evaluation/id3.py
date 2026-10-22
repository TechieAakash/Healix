"""Compact, dependency-free binary ID3 baseline for DDXPlus coursework evaluation."""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Sequence, Set


def _entropy(counts: Counter) -> float:
    total = sum(counts.values())
    if not total:
        return 0.0
    return -sum((n / total) * math.log2(n / total) for n in counts.values() if n)


class ID3Classifier:
    """Binary-feature ID3 with deterministic ties, depth and leaf-size limits."""

    def __init__(self, max_depth: int = 7, min_leaf: int = 20, max_features: int = 96):
        self.max_depth = max_depth
        self.min_leaf = min_leaf
        self.max_features = max_features
        self.tree: Dict[str, Any] = {}
        self.labels: List[str] = []
        self.node_count = 0
        self.training_examples = 0

    def fit(self, examples: Sequence[tuple[Set[str], str]]) -> "ID3Classifier":
        self.training_examples = len(examples)
        self.labels = sorted({label for _, label in examples})
        frequencies = Counter(feature for features, _ in examples for feature in features)
        attributes = [feature for feature, _ in sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))[:self.max_features]]
        self.tree = self._build(examples, attributes, 0)
        return self

    def _build(self, examples: Sequence[tuple[Set[str], str]], attributes: Sequence[str], depth: int) -> Dict[str, Any]:
        counts = Counter(label for _, label in examples)
        self.node_count += 1
        if len(counts) <= 1 or depth >= self.max_depth or len(examples) < 2 * self.min_leaf or not attributes:
            return {"leaf": True, "counts": dict(counts)}
        parent_entropy = _entropy(counts)
        best_gain, best_feature = 0.0, None
        for feature in attributes:
            yes = Counter(label for features, label in examples if feature in features)
            no = counts - yes
            n_yes, n_no = sum(yes.values()), sum(no.values())
            if min(n_yes, n_no) < self.min_leaf:
                continue
            gain = parent_entropy - (n_yes / len(examples)) * _entropy(yes) - (n_no / len(examples)) * _entropy(no)
            if gain > best_gain + 1e-12 or (abs(gain - best_gain) <= 1e-12 and best_feature is not None and feature < best_feature):
                best_gain, best_feature = gain, feature
        if best_feature is None:
            return {"leaf": True, "counts": dict(counts)}
        yes_rows = [row for row in examples if best_feature in row[0]]
        no_rows = [row for row in examples if best_feature not in row[0]]
        remaining = [feature for feature in attributes if feature != best_feature]
        return {
            "leaf": False,
            "feature": best_feature,
            "gain": best_gain,
            "yes": self._build(yes_rows, remaining, depth + 1),
            "no": self._build(no_rows, remaining, depth + 1),
            "fallback": dict(counts),
        }

    def predict_proba(self, features: Set[str]) -> Dict[str, float]:
        node = self.tree
        while not node.get("leaf"):
            node = node["yes"] if node["feature"] in features else node["no"]
        counts = node.get("counts") or {}
        total = sum(counts.values()) or 1
        return {label: counts.get(label, 0) / total for label in self.labels}

    def predict(self, features: Set[str], k: int = 5) -> List[str]:
        probabilities = self.predict_proba(features)
        return sorted(probabilities, key=lambda label: (-probabilities[label], label))[:k]

    def serialize(self) -> Dict[str, Any]:
        return {
            "model": "hand_written_id3",
            "max_depth": self.max_depth,
            "min_leaf": self.min_leaf,
            "max_features": self.max_features,
            "labels": self.labels,
            "training_examples": self.training_examples,
            "node_count": self.node_count,
            "tree": self.tree,
        }


def stratified_sample(rows: Iterable[Dict[str, str]], per_class: int = 200, seed: int = 17):
    rng = random.Random(seed)
    samples: Dict[str, List[tuple[Set[str], str]]] = defaultdict(list)
    seen = Counter()
    from scripts.train_ddxplus_nb import features
    for row in rows:
        label = row["PATHOLOGY"]
        seen[label] += 1
        item = (features(row), label)
        bucket = samples[label]
        if len(bucket) < per_class:
            bucket.append(item)
        else:
            slot = rng.randrange(seen[label])
            if slot < per_class:
                bucket[slot] = item
    return [example for label in sorted(samples) for example in samples[label]]
