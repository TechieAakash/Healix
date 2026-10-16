"""
Command line entry point for Healix medical knowledge base ingestion:
Usage: python -m app.ai.ingest
"""

import asyncio
from app.services.ai.rag.ingest import run_cli_ingest

if __name__ == "__main__":
    asyncio.run(run_cli_ingest())
