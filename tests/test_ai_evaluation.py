"""
Integration Test running the Healix AI Evaluation Benchmark.
Asserts 100% pass rate on safety and benchmark evaluation test cases.
"""

import pytest
from app.services.ai.evaluation.evaluator import AIEvaluator


@pytest.mark.asyncio
async def test_full_ai_benchmark_evaluation():
    evaluator = AIEvaluator()
    summary = await evaluator.run_evaluation()

    assert summary["total_cases"] >= 10
    assert summary["failed"] == 0
    assert summary["pass_rate_pct"] == 100.0
