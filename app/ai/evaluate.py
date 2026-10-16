"""
CLI Entrypoint for Healix AI Evaluation Suite:
Usage: python -m app.ai.evaluate
"""

import asyncio
from app.services.ai.evaluation.evaluator import run_cli_eval

if __name__ == "__main__":
    asyncio.run(run_cli_eval())
