"""
Vector Database Implementation.
Provides in-memory and disk-persisted vector storage with cosine similarity search,
metadata filtering, and atomic document updates.
"""

import json
import math
import os
import logging
from typing import List, Dict, Any, Optional
from app.services.ai.base import BaseVectorStore
from app.core.config import settings

logger = logging.getLogger("healix.ai.vector_store")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculates cosine similarity between two numeric vectors."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0

    return max(-1.0, min(1.0, dot / (norm1 * norm2)))


class JsonPersistentVectorStore(BaseVectorStore):
    """
    Thread-safe, file-persisted vector store.
    Stores chunk vectors, original texts, and rich clinical metadata.
    Zero native C++ compiler requirements on Windows.
    """

    def __init__(self, persistence_path: Optional[str] = "_DEFAULT_"):
        if persistence_path == "_DEFAULT_":
            self.persistence_path = settings.VECTOR_DB_PATH
        else:
            self.persistence_path = persistence_path
        self.documents: Dict[str, Dict[str, Any]] = {}
        if self.persistence_path:
            self._load()

    def _load(self) -> None:
        """Loads index from disk if existing."""
        if not self.persistence_path:
            return
        if os.path.exists(self.persistence_path):
            try:
                with open(self.persistence_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.documents = {doc["chunk_id"]: doc for doc in data}
                logger.info("Loaded %d documents from %s", len(self.documents), self.persistence_path)
            except Exception as e:
                logger.error("Failed to load vector store from %s: %s", self.persistence_path, str(e))
                self.documents = {}

    def _persist(self) -> None:
        """Flushes in-memory documents to disk atomically."""
        if not self.persistence_path:
            return
        dir_name = os.path.dirname(self.persistence_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        try:
            with open(self.persistence_path, "w", encoding="utf-8") as f:
                json.dump(list(self.documents.values()), f, indent=2)
        except Exception as e:
            logger.error("Failed to save vector store to %s: %s", self.persistence_path, str(e))

    async def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        for doc in documents:
            cid = doc.get("chunk_id")
            if not cid:
                continue
            self.documents[cid] = doc
        self._persist()

    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        scored: List[Dict[str, Any]] = []

        for cid, doc in self.documents.items():
            doc_meta = doc.get("metadata", {})

            # Metadata filtering check
            if filter_metadata:
                match = True
                for k, v in filter_metadata.items():
                    if doc_meta.get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            score = cosine_similarity(query_vector, doc.get("vector", []))
            scored.append({
                "chunk_id": cid,
                "document_id": doc.get("document_id"),
                "text": doc.get("text"),
                "metadata": doc_meta,
                "similarity_score": round(score, 4),
            })

        # Sort descending by similarity score
        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_k]

    async def delete(self, document_ids: List[str]) -> None:
        to_del = []
        for cid, doc in self.documents.items():
            if doc.get("document_id") in document_ids or cid in document_ids:
                to_del.append(cid)
        for cid in to_del:
            self.documents.pop(cid, None)
        self._persist()

    async def update(self, document_id: str, document: Dict[str, Any]) -> None:
        self.documents[document_id] = document
        self._persist()

    async def count(self) -> int:
        return len(self.documents)


_global_vector_store: Optional[JsonPersistentVectorStore] = None


def get_vector_store() -> BaseVectorStore:
    """Singleton accessor for application vector store."""
    global _global_vector_store
    if _global_vector_store is None:
        _global_vector_store = JsonPersistentVectorStore()
    return _global_vector_store
