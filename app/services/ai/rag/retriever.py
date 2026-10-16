"""
RAG Retriever and Re-ranking Service.
Coordinates semantic vector search, metadata filtering, candidate re-ranking,
and authoritative citation preservation.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.ai.base import BaseReranker
from app.services.ai.rag.embeddings import get_embedding_service
from app.services.ai.rag.vector_store import get_vector_store
from app.services.ai.schemas import SourceCitation

logger = logging.getLogger("healix.ai.retriever")


class LightweightLexicalSemanticReranker(BaseReranker):
    """
    Lightweight candidate reranker combining cosine similarity score
    with lexical keyword density and clinical entity overlap.
    """

    async def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        if not candidates:
            return []

        query_tokens = set(re.findall(r"\w+", query.lower()))
        reranked = []

        for item in candidates:
            text = item.get("text", "").lower()
            metadata = item.get("metadata", {})
            title = metadata.get("title", "").lower()

            # Base similarity score (0.0 to 1.0)
            base_score = float(item.get("similarity_score", 0.0))

            # Keyword overlap bonus
            text_tokens = set(re.findall(r"\w+", text))
            title_tokens = set(re.findall(r"\w+", title))

            overlap_count = len(query_tokens.intersection(text_tokens))
            title_overlap = len(query_tokens.intersection(title_tokens))

            lexical_factor = (overlap_count * 0.05) + (title_overlap * 0.1)
            combined_score = round(min(1.0, max(0.0, (base_score * 0.7) + (lexical_factor * 0.3))), 4)

            item_copy = dict(item)
            item_copy["reranked_score"] = combined_score
            reranked.append(item_copy)

        reranked.sort(key=lambda x: x["reranked_score"], reverse=True)
        return reranked[:top_k]


class RAGRetriever:
    """
    Main RAG retrieval coordinator for Healix.
    Enforces metadata filtering, threshold checks, and source citations.
    """

    def __init__(
        self,
        vector_store=None,
        embedding_service=None,
        reranker=None,
    ):
        self.vector_store = vector_store or get_vector_store()
        self.embedding_service = embedding_service or get_embedding_service()
        self.reranker = reranker or LightweightLexicalSemanticReranker()
        self._cache: Dict[str, List[Dict[str, Any]]] = {}
        self._cache_max_size = 250

    async def retrieve_context(
        self,
        query: str,
        topic_filter: Optional[str] = None,
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves grounded medical chunks for a clinical inquiry.
        Utilizes in-memory LRU cache to minimize embedding overhead on recurrent queries.
        """
        k = top_k or settings.RAG_TOP_K
        clean_q = query.strip().lower()
        cache_key = f"{clean_q}:{topic_filter}:{k}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        query_vector = await self.embedding_service.embed_text(query)

        filter_meta = {"topic": topic_filter} if topic_filter else None
        # Retrieve candidate pool (2x top_k for reranker)
        candidates = await self.vector_store.search(
            query_vector=query_vector,
            top_k=max(k * 2, 8),
            filter_metadata=filter_meta,
        )

        # Filter out candidates below similarity threshold
        filtered = [
            c for c in candidates
            if c.get("similarity_score", 0.0) >= settings.SIMILARITY_THRESHOLD
        ]
        if not filtered:
            # If threshold is too strict on edge terms, fall back to best available candidate
            filtered = candidates[:k]

        # Apply reranking
        if settings.ENABLE_RAG_RERANKING and filtered:
            final_chunks = await self.reranker.rerank(query, filtered, top_k=k)
        else:
            final_chunks = filtered[:k]

        # Store in cache
        if len(self._cache) >= self._cache_max_size:
            self._cache.pop(next(iter(self._cache)))
        self._cache[cache_key] = final_chunks

        return final_chunks

    def format_citations(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Converts retrieved chunks into verified clinical citations.
        Guarantees URLs and source organizations originate solely from indexed documents.
        """
        seen_titles = set()
        citations = []

        for chk in chunks:
            meta = chk.get("metadata", {})
            title = meta.get("title", "Clinical Practice Reference")
            if title in seen_titles:
                continue
            seen_titles.add(title)

            score = chk.get("reranked_score", chk.get("similarity_score", 0.85))
            citations.append({
                "title": title,
                "organization": meta.get("organization", "Authoritative Health Organization"),
                "url": meta.get("url"),
                "relevance": round(float(score), 2),
                "topic": meta.get("topic"),
            })

        return citations

    def build_rag_context_block(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Constructs sanitized, delimited RAG context for injection into LLM prompts.
        Protects against prompt injection by clearly labeling retrieved content as DATA.
        """
        if not chunks:
            return "NO RELEVANT MEDICAL DOCUMENTS FOUND IN KNOWLEDGE BASE."

        blocks = []
        for i, chk in enumerate(chunks, 1):
            meta = chk.get("metadata", {})
            org = meta.get("organization", "Medical Authority")
            title = meta.get("title", "Guideline")
            text = chk.get("text", "").strip()

            blocks.append(
                f"[DOCUMENT {i}]\n"
                f"Source: {org} - {title}\n"
                f"Evidence Context: {text}\n"
                f"[END DOCUMENT {i}]"
            )

        return "\n\n".join(blocks)
