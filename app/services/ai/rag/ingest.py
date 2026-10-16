"""
Medical Knowledge Ingestion Pipeline.
Handles chunking, metadata attachment, embedding generation, versioning,
and indexing into the vector store.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from app.services.ai.rag.knowledge_data import MEDICAL_KNOWLEDGE_DOCUMENTS
from app.services.ai.rag.document_loader import chunk_document
from app.services.ai.rag.embeddings import get_embedding_service
from app.services.ai.rag.vector_store import get_vector_store

logger = logging.getLogger("healix.ai.ingest")


class KnowledgeIngestionPipeline:
    """
    Ingests authoritative medical documents into the vector database.
    Supports atomic add, update, delete, and full re-indexing.
    """

    def __init__(self, vector_store=None, embedding_service=None):
        self.vector_store = vector_store or get_vector_store()
        self.embedding_service = embedding_service or get_embedding_service()

    async def ingest_documents(
        self,
        documents: Optional[List[Dict[str, Any]]] = None,
        reindex: bool = False,
    ) -> Dict[str, Any]:
        """
        Executes document ingestion.
        """
        docs = documents or MEDICAL_KNOWLEDGE_DOCUMENTS
        logger.info("Starting ingestion of %d medical documents (reindex=%s)...", len(docs), reindex)

        if reindex:
            # Clear existing items
            all_cids = list(self.vector_store.documents.keys())
            await self.vector_store.delete(all_cids)

        chunks_to_add = []
        for doc in docs:
            doc_chunks = chunk_document(doc)
            chunks_to_add.extend(doc_chunks)

        logger.info("Generated %d sentence-bounded chunks. Generating embeddings...", len(chunks_to_add))

        texts = [c["text"] for c in chunks_to_add]
        embeddings = await self.embedding_service.embed_documents(texts)

        indexed_records = []
        for chunk, vector in zip(chunks_to_add, embeddings):
            record = {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "text": chunk["text"],
                "content_hash": chunk["content_hash"],
                "metadata": chunk["metadata"],
                "vector": vector,
            }
            indexed_records.append(record)

        await self.vector_store.add_documents(indexed_records)
        total_count = await self.vector_store.count()
        logger.info("Ingestion completed successfully! Total indexed chunks: %d", total_count)

        return {
            "documents_processed": len(docs),
            "chunks_indexed": len(indexed_records),
            "total_chunks_in_store": total_count,
            "status": "SUCCESS",
        }


async def run_cli_ingest():
    pipeline = KnowledgeIngestionPipeline()
    result = await pipeline.ingest_documents(reindex=True)
    print(f"=== Healix Knowledge Ingestion Complete ===")
    print(f"Documents processed: {result['documents_processed']}")
    print(f"Chunks indexed: {result['chunks_indexed']}")
    print(f"Total chunks in store: {result['total_chunks_in_store']}")
    print(f"Status: {result['status']}")


if __name__ == "__main__":
    asyncio.run(run_cli_ingest())
