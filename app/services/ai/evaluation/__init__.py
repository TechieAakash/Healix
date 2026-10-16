"""
AI Evaluation package.
"""

from app.services.ai.evaluation.dataset import EVALUATION_TEST_CASES
from app.services.ai.evaluation.evaluator import AIEvaluator, run_cli_eval

__all__ = [
    "EVALUATION_TEST_CASES",
    "AIEvaluator",
    "run_cli_eval",
]
