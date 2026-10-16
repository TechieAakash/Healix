from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class RAGService(ABC):
    """
    Abstract interface for Phase 2 Retrieval-Augmented Generation (RAG).
    Will query vector databases (e.g., Chroma, pgvector, FAISS)
    containing peer-reviewed medical journals and clinical guidelines.
    """

    @abstractmethod
    async def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant medical document chunks based on embedding similarity."""
        pass

    @abstractmethod
    async def format_citations(self, document_ids: List[str]) -> List[Dict[str, Any]]:
        """Format retrieved documents into verified medical citations."""
        pass


class MockRAGService(RAGService):
    """Placeholder mock RAG service for Phase 1 testing."""

    async def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Clinical Practice Guidelines for Tension Headache",
                "source": "Mayo Clinic",
                "retrieved_context": "Bilateral, non-throbbing cranial sensation responding to rest and hydration.",
                "similarity_score": 0.92,
            }
        ]

    async def format_citations(self, document_ids: List[str]) -> List[Dict[str, Any]]:
        return [
            {
                "name": "Mayo Clinic",
                "url": "https://www.mayoclinic.org",
                "authority": "Reviewed by Clinical Neurology Panel",
            }
        ]
