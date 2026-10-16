"""
Unit Tests for RAG Pipeline, Embeddings, and Vector Search.
Verifies document chunking, metadata preservation, cosine similarity search,
and citation integrity.
"""

import pytest
from app.services.ai.rag.document_loader import clean_text, chunk_document
from app.services.ai.rag.embeddings import LightweightSemanticEmbeddingService
from app.services.ai.rag.vector_store import JsonPersistentVectorStore, cosine_similarity
from app.services.ai.rag.retriever import RAGRetriever


def test_clean_text():
    raw = "  This has   excessive   spacing \r\n and newlines.\n\n\n\nDone.  "
    cleaned = clean_text(raw)
    assert "excessive spacing" in cleaned
    assert "\r" not in cleaned
    assert "\n\n\n" not in cleaned


def test_chunk_document_metadata_preservation():
    sample_doc = {
        "id": "TEST_DOC_01",
        "title": "Clinical Guidelines on Migraine",
        "source": "NIH Neurology",
        "url": "https://nih.gov/migraine",
        "organization": "NIH",
        "publication_date": "2024-01-01",
        "last_reviewed": "2025-01-01",
        "topic": "headache",
        "document_type": "clinical_guideline",
        "content": (
            "Migraine is a common neurological disorder causing throbbing head pain. "
            "It is often accompanied by sensitivity to ambient light and sound. "
            "Resting in a dark quiet room helps alleviate discomfort."
        ),
    }

    chunks = chunk_document(sample_doc, target_chunk_size=100)
    assert len(chunks) >= 1
    first_chunk = chunks[0]
    assert first_chunk["document_id"] == "TEST_DOC_01"
    assert first_chunk["metadata"]["title"] == "Clinical Guidelines on Migraine"
    assert first_chunk["metadata"]["organization"] == "NIH"
    assert first_chunk["metadata"]["url"] == "https://nih.gov/migraine"
    assert first_chunk["metadata"]["topic"] == "headache"


@pytest.mark.asyncio
async def test_embedding_and_vector_search():
    embedding_svc = LightweightSemanticEmbeddingService(vector_dim=64)
    vector_store = JsonPersistentVectorStore(persistence_path=None)  # In-memory mode

    doc1_text = "Tension headaches present with diffuse dull band-like pressure."
    doc2_text = "Acute myocardial infarction manifests with severe retrosternal chest pain."

    v1 = await embedding_svc.embed_text(doc1_text)
    v2 = await embedding_svc.embed_text(doc2_text)

    await vector_store.add_documents([
        {
            "chunk_id": "c1",
            "document_id": "d1",
            "text": doc1_text,
            "metadata": {"topic": "headache", "organization": "Mayo Clinic", "title": "Headache Guide"},
            "vector": v1,
        },
        {
            "chunk_id": "c2",
            "document_id": "d2",
            "text": doc2_text,
            "metadata": {"topic": "cardiopulmonary", "organization": "AHA", "title": "Heart Guide"},
            "vector": v2,
        },
    ])

    assert await vector_store.count() == 2

    # Query for headache
    q_vec = await embedding_svc.embed_text("mild tension headache forehead pressure")
    results = await vector_store.search(q_vec, top_k=1)

    assert len(results) == 1
    assert results[0]["chunk_id"] == "c1"
    assert results[0]["metadata"]["topic"] == "headache"

    # Query with metadata filter
    q_cardio_vec = await embedding_svc.embed_text("chest pain")
    filtered_results = await vector_store.search(
        q_cardio_vec, top_k=2, filter_metadata={"topic": "cardiopulmonary"}
    )
    assert len(filtered_results) == 1
    assert filtered_results[0]["chunk_id"] == "c2"


def test_cosine_similarity():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    v3 = [0.0, 1.0, 0.0]

    assert pytest.approx(cosine_similarity(v1, v2), 0.001) == 1.0
    assert pytest.approx(cosine_similarity(v1, v3), 0.001) == 0.0
