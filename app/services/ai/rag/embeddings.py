"""
Embedding Services.
Provides configurable vector generation using OpenAI embeddings or an offline
lightweight semantic subword/bag-of-words vectorizer for deterministic local operation.
"""

import math
import re
import logging
from typing import List, Dict, Optional
import httpx
from app.core.config import settings
from app.services.ai.base import BaseEmbeddingService

logger = logging.getLogger("healix.ai.embeddings")


class LightweightSemanticEmbeddingService(BaseEmbeddingService):
    """
    Deterministic zero-dependency local embedding service.
    Creates normalized subword-character and token semantic vectors.
    Allows full vector search and RAG operation completely offline or during tests.
    """

    def __init__(self, vector_dim: int = 512):
        self._dim = vector_dim

    @property
    def dimension(self) -> int:
        return self._dim

    def _hash_token(self, token: str) -> int:
        # FNV-1a hash variant
        h = 2166136261
        for ch in token:
            h = (h ^ ord(ch)) * 16777619
            h &= 0xFFFFFFFF
        return h

    def _text_to_vector(self, text: str) -> List[float]:
        vec = [0.0] * self._dim
        tokens = re.findall(r"\w+", text.lower())
        if not tokens:
            return vec

        for t in tokens:
            # Hash full token
            idx = self._hash_token(t) % self._dim
            vec[idx] += 1.0

            # Subword 3-grams for semantic fuzzy matches
            if len(t) >= 3:
                for i in range(len(t) - 2):
                    sub = t[i : i + 3]
                    s_idx = self._hash_token(sub) % self._dim
                    vec[s_idx] += 0.5

        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [round(x / norm, 6) for x in vec]
        return vec

    async def embed_text(self, text: str) -> List[float]:
        return self._text_to_vector(text)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._text_to_vector(t) for t in texts]


class OpenAIEmbeddingService(BaseEmbeddingService):
    """
    Production embedding service connecting to OpenAI or compatible API endpoints.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model or settings.EMBEDDING_MODEL
        self.base_url = (base_url or settings.AI_BASE_URL or "https://api.openai.com/v1").rstrip("/")
        self._dimension = 1536  # Default for text-embedding-3-small

    @property
    def dimension(self) -> int:
        return self._dimension

    async def embed_text(self, text: str) -> List[float]:
        results = await self.embed_documents([text])
        return results[0] if results else [0.0] * self._dimension

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not self.api_key:
            logger.warning("No AI_API_KEY provided for OpenAI embeddings. Falling back to local embeddings.")
            fallback = LightweightSemanticEmbeddingService()
            return await fallback.embed_documents(texts)

        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "input": texts,
            }
            try:
                resp = await client.post(
                    f"{self.base_url}/embeddings",
                    headers=headers,
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                sorted_items = sorted(data["data"], key=lambda x: x["index"])
                vectors = [item["embedding"] for item in sorted_items]
                if vectors:
                    self._dimension = len(vectors[0])
                return vectors
            except Exception as e:
                logger.error("Failed to fetch OpenAI embeddings (%s). Using local fallback.", str(e))
                fallback = LightweightSemanticEmbeddingService()
                return await fallback.embed_documents(texts)


def get_embedding_service() -> BaseEmbeddingService:
    """Factory resolving configured embedding provider."""
    provider = settings.AI_PROVIDER.lower()
    if provider in ("openai", "azure") and settings.AI_API_KEY:
        return OpenAIEmbeddingService()
    return LightweightSemanticEmbeddingService()
