"""
RAG package initialization.
"""

from app.services.ai.rag.embeddings import (
    BaseEmbeddingService,
    OpenAIEmbeddingService,
    LightweightSemanticEmbeddingService,
    get_embedding_service,
)
from app.services.ai.rag.vector_store import (
    BaseVectorStore,
    JsonPersistentVectorStore,
    get_vector_store,
)
from app.services.ai.rag.retriever import RAGRetriever, LightweightLexicalSemanticReranker
from app.services.ai.rag.document_loader import chunk_document, clean_text
from app.services.ai.rag.ingest import KnowledgeIngestionPipeline

__all__ = [
    "BaseEmbeddingService",
    "OpenAIEmbeddingService",
    "LightweightSemanticEmbeddingService",
    "get_embedding_service",
    "BaseVectorStore",
    "JsonPersistentVectorStore",
    "get_vector_store",
    "RAGRetriever",
    "LightweightLexicalSemanticReranker",
    "chunk_document",
    "clean_text",
    "KnowledgeIngestionPipeline",
]
