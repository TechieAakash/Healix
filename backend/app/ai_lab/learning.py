from __future__ import annotations
import math
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DecisionTreeNode(BaseModel):
    attribute: Optional[str] = None
    value: Optional[str] = None
    label: Optional[str] = None
    entropy: float = 0.0
    samples_count: int = 0
    children: Dict[str, DecisionTreeNode] = Field(default_factory=dict)

class ID3TrainResult(BaseModel):
    root_entropy: float
    feature_gains: Dict[str, float]
    tree: DecisionTreeNode
    training_samples_count: int
    features: List[str]

class ID3Learner:
    """
    Implements Unit 5: ID3 Decision Tree Induction using Shannon Entropy & Information Gain.
    """

    @classmethod
    def calculate_entropy(cls, labels: List[str]) -> float:
        if not labels:
            return 0.0
        total = len(labels)
        counts = {}
        for l in labels:
            counts[l] = counts.get(l, 0) + 1

        ent = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                ent -= p * math.log2(p)
        return round(ent, 4)

    @classmethod
    def calculate_information_gain(
        cls,
        data: List[Dict[str, str]],
        target_attr: str,
        split_attr: str
    ) -> float:
        total_entropy = cls.calculate_entropy([row[target_attr] for row in data])
        total_samples = len(data)

        # Partition by split_attr
        partitions: Dict[str, List[str]] = {}
        for row in data:
            val = row[split_attr]
            partitions.setdefault(val, []).append(row[target_attr])

        subset_entropy = 0.0
        for subset_labels in partitions.values():
            subset_entropy += (len(subset_labels) / total_samples) * cls.calculate_entropy(subset_labels)

        return round(total_entropy - subset_entropy, 4)

    @classmethod
    def build_tree(
        cls,
        data: List[Dict[str, str]],
        features: List[str],
        target_attr: str
    ) -> DecisionTreeNode:
        labels = [row[target_attr] for row in data]

        # Base case 1: all same label
        if len(set(labels)) <= 1:
            return DecisionTreeNode(
                label=labels[0] if labels else "Unknown",
                entropy=0.0,
                samples_count=len(data)
            )

        # Base case 2: no features left
        if not features:
            majority = max(set(labels), key=labels.count)
            return DecisionTreeNode(
                label=majority,
                entropy=cls.calculate_entropy(labels),
                samples_count=len(data)
            )

        # Find feature with maximum information gain
        best_feature = None
        best_gain = -1.0

        for f in features:
            gain = cls.calculate_information_gain(data, target_attr, f)
            if gain > best_gain:
                best_gain = gain
                best_feature = f

        node = DecisionTreeNode(
            attribute=best_feature,
            entropy=cls.calculate_entropy(labels),
            samples_count=len(data)
        )

        remaining_features = [f for f in features if f != best_feature]

        # Group data by best_feature values
        partitions: Dict[str, List[Dict[str, str]]] = {}
        for row in data:
            val = row[best_feature]
            partitions.setdefault(val, []).append(row)

        for val, subset in partitions.items():
            child_node = cls.build_tree(subset, remaining_features, target_attr)
            child_node.value = val
            node.children[val] = child_node

        return node

    @classmethod
    def train_clinical_demo(cls) -> ID3TrainResult:
        # Synthetic symptom triage training set
        dataset = [
            {"Fever": "High", "Cough": "Dry", "SoreThroat": "Yes", "Triage": "Viral_Infection"},
            {"Fever": "High", "Cough": "Productive", "SoreThroat": "No", "Triage": "Bacterial_Infection"},
            {"Fever": "Mild", "Cough": "Dry", "SoreThroat": "Yes", "Triage": "Viral_Infection"},
            {"Fever": "None", "Cough": "Dry", "SoreThroat": "No", "Triage": "Allergy"},
            {"Fever": "High", "Cough": "Productive", "SoreThroat": "Yes", "Triage": "Bacterial_Infection"},
            {"Fever": "None", "Cough": "Productive", "SoreThroat": "No", "Triage": "Bronchitis"},
            {"Fever": "Mild", "Cough": "Productive", "SoreThroat": "No", "Triage": "Bronchitis"},
            {"Fever": "High", "Cough": "Dry", "SoreThroat": "No", "Triage": "Viral_Infection"},
        ]
        features = ["Fever", "Cough", "SoreThroat"]
        target = "Triage"

        root_ent = cls.calculate_entropy([r[target] for r in dataset])
        gains = {f: cls.calculate_information_gain(dataset, target, f) for f in features}
        tree = cls.build_tree(dataset, features, target)

        return ID3TrainResult(
            root_entropy=root_ent,
            feature_gains=gains,
            tree=tree,
            training_samples_count=len(dataset),
            features=features
        )

