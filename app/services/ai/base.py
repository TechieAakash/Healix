"""
Core Base Interfaces for Healix AI Layer.
Defines modular abstractions for LLM providers, embedding services,
vector stores, rerankers, and orchestrators.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMResponse(BaseModel):
    text: str
    usage: Optional[LLMUsage] = None
    model: str = ""
    finish_reason: Optional[str] = None


class BaseLLMProvider(ABC):
    """
    Provider-agnostic LLM interface supporting text, structured output, and chat.
    Configurable via environment variables without affecting business logic.
    """

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Generates raw text response."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        schema: Type[T],
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 2,
    ) -> T:
        """
        Generates response guaranteed to match the Pydantic schema.
        Performs controlled retries if schema validation fails.
        """
        pass

    @abstractmethod
    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Generates response for a conversation thread."""
        pass


class BaseEmbeddingService(ABC):
    """
    Abstraction for text embedding generation.
    Supports pluggable embedding models (OpenAI, HuggingFace, lightweight semantic).
    """

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Embed a single string."""
        pass

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of document strings."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Returns embedding vector dimension."""
        pass


class BaseVectorStore(ABC):
    """
    Interface for vector database operations (search, add, delete, update).
    Supports semantic retrieval with metadata filtering.
    """

    @abstractmethod
    async def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents with pre-computed embeddings and metadata.
        Each document expects: {id, text, vector, metadata}
        """
        pass

    @abstractmethod
    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for top_k most similar document chunks.
        Returns list of chunks with similarity scores.
        """
        pass

    @abstractmethod
    async def delete(self, document_ids: List[str]) -> None:
        """Remove documents by IDs."""
        pass

    @abstractmethod
    async def update(self, document_id: str, document: Dict[str, Any]) -> None:
        """Update an existing document."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Return total indexed chunks."""
        pass


class BaseReranker(ABC):
    """
    Lightweight re-ranking abstraction to score and order candidate chunks.
    """

    @abstractmethod
    async def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """Reranks candidate chunks by relevance to query."""
        pass
