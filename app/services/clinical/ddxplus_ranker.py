"""Offline Naive Bayes ranking over explicitly mapped DDXPlus evidence only."""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.services.clinical.evidence_mapper import evidence_mapper


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "data" / "models" / "ddxplus_nb.json"
CALIBRATION_PATH = PROJECT_ROOT / "data" / "models" / "ddxplus_calibration.json"


@lru_cache(maxsize=1)
def load_model() -> Dict[str, Any]:
    with MODEL_PATH.open(encoding="utf-8") as source:
        return json.load(source)


@lru_cache(maxsize=1)
def load_calibration() -> Dict[str, Any]:
    try:
        with CALIBRATION_PATH.open(encoding="utf-8") as source:
            return json.load(source)
    except FileNotFoundError:
        return {"valid": False, "reason": "Calibration has not been measured."}


def _base_code(token: str) -> str:
    return token.split("_@_")[0]


def _softmax(scores: Dict[str, float], temperature: float) -> Dict[str, float]:
    temperature = max(1e-6, float(temperature))
    scaled = {label: score / temperature for label, score in scores.items()}
    peak = max(scaled.values())
    values = {label: math.exp(score - peak) for label, score in scaled.items()}
    total = sum(values.values())
    return {label: value / total for label, value in values.items()}


class DDXPlusRanker:
    """Single condition node with independent positive evidence children.

    Unknown findings are omitted. DDXPlus does not encode general negative
    findings, so absence is never treated as a negative likelihood.
    """

    def __init__(self, model: Optional[Dict[str, Any]] = None, calibration: Optional[Dict[str, Any]] = None):
        self.model = model or load_model()
        self.calibration = calibration or load_calibration()
        self.alpha = float(self.model.get("alpha", 0.25))

    def _scores(self, evidence: Dict[str, float]) -> tuple[Dict[str, float], Dict[str, Dict[str, float]]]:
        classes = self.model["classes"]
        token_counts = self.model["token_counts"]
        n = float(self.model["training_rows"])
        scores: Dict[str, float] = {}
        contributions: Dict[str, Dict[str, float]] = {}
        for label, count in classes.items():
            score = math.log(max(count / n, 1e-15))
            label_contributions = {}
            for token, weight in evidence.items():
                if weight <= 0:
                    continue
                # The training artifact stores feature presence counts. A
                # Bernoulli child probability is estimated per pathology.
                probability = (token_counts[label].get(token, 0) + self.alpha) / (count + 2 * self.alpha)
                contribution = float(weight) * math.log(max(probability, 1e-15))
                score += contribution
                label_contributions[token] = contribution
            scores[label] = score
            contributions[label] = label_contributions
        return scores, contributions

    def rank(self, evidence: Optional[Dict[str, float]] = None, *, min_evidence: Optional[int] = None) -> Dict[str, Any]:
        evidence = evidence or {}
        supported_codes = set(evidence_mapper.definitions)
        evidence_count = len({_base_code(code) for code, weight in evidence.items() if weight > 0 and _base_code(code) in supported_codes})
        calibration = self.calibration
        if not calibration.get("valid"):
            return {"abstain": True, "reason": "calibration_unavailable", "ranked_conditions": [], "evidence_count": evidence_count}
        minimum = int(min_evidence if min_evidence is not None else calibration.get("min_evidence", 3))
        if evidence_count < minimum:
            return {"abstain": True, "reason": "insufficient_mapped_evidence", "ranked_conditions": [], "evidence_count": evidence_count}
        scores, contributions = self._scores(evidence)
        probabilities = _softmax(scores, calibration.get("temperature", 1.0))
        ordered = sorted(probabilities, key=probabilities.get, reverse=True)
        top_probability = probabilities[ordered[0]]
        threshold = float(calibration.get("min_top_probability", 0.55))
        if top_probability < threshold:
            return {"abstain": True, "reason": "low_calibrated_confidence", "ranked_conditions": [], "evidence_count": evidence_count, "top_probability": top_probability}
        band_thresholds = calibration.get("confidence_bands", {"moderate": 0.55, "high": 0.8})
        band = "high" if top_probability >= band_thresholds.get("high", 0.8) else "moderate" if top_probability >= band_thresholds.get("moderate", 0.55) else "low"
        ranked = []
        for label in ordered[:5]:
            ranked.append({
                "condition": label,
                "probability": probabilities[label],
                "confidence_band": band if label == ordered[0] else "low",
                "log_likelihood_contributions": [
                    {"evidence_code": code, "contribution": value}
                    for code, value in sorted(contributions[label].items(), key=lambda item: abs(item[1]), reverse=True)
                ],
            })
        return {"abstain": False, "reason": None, "ranked_conditions": ranked, "evidence_count": evidence_count, "calibrated": True, "synthetic_data_notice": "Pattern matches from synthetic DDXPlus cases; not a diagnosis."}

    def analyze(self, description: str = "", symptoms: Optional[List[Dict[str, Any]]] = None, answers: Optional[List[Dict[str, Any]]] = None, *, age: Optional[int] = None, sex: Optional[str] = None) -> Dict[str, Any]:
        mapped = evidence_mapper.map_assessment(description, symptoms, answers, age=age, sex=sex)
        ranking = self.rank(mapped["evidence"])
        return {"mapping": mapped, "ranking": ranking}


ddxplus_ranker = DDXPlusRanker()
