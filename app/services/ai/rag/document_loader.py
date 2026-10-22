"""
Medical Document Loader, Cleaner, and Sentence-Aware Chunker.
Splits clinical guidelines into coherent segments while preserving rich source metadata.
"""

import hashlib
import re
from typing import List, Dict, Any


def clean_text(text: str) -> str:
    """Cleans text of aberrant characters, excessive whitespace, and standardizes punctuation."""
    if not text:
        return ""
    # Normalize unicode spaces and quotes
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def calculate_content_hash(text: str) -> str:
    """Computes SHA-256 hash for document version tracking."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def chunk_document(
    doc: Dict[str, Any],
    target_chunk_size: int = 350,
    overlap_chars: int = 50,
) -> List[Dict[str, Any]]:
    """
    Sentence-aware chunking preserving all document metadata.
    Does not split sentences across chunk boundaries if possible.
    """
    raw_content = clean_text(doc.get("content", ""))
    doc_id = doc.get("id", "DOC_UNKNOWN")
    doc_hash = calculate_content_hash(raw_content)

    # Split into sentences using punctuation boundaries
    sentence_regex = r"(?<=[.!?])\s+"
    sentences = [s.strip() for s in re.split(sentence_regex, raw_content) if s.strip()]
    bounded_sentences = []
    for sentence in sentences:
        if len(sentence) <= target_chunk_size:
            bounded_sentences.append(sentence)
            continue
        # Keep the configured chunk ceiling even when a source contains a
        # very long sentence, splitting only at word boundaries.
        words, fragment = sentence.split(), []
        for word in words:
            candidate = " ".join(fragment + [word])
            if fragment and len(candidate) > target_chunk_size:
                bounded_sentences.append(" ".join(fragment))
                fragment = [word]
            else:
                fragment.append(word)
        if fragment:
            bounded_sentences.append(" ".join(fragment))
    sentences = bounded_sentences

    chunks = []
    current_sentences = []
    current_len = 0
    chunk_idx = 0

    for sentence in sentences:
        sent_len = len(sentence)
        if current_sentences and (current_len + sent_len > target_chunk_size):
            chunk_text = " ".join(current_sentences)
            chunks.append({
                "chunk_id": f"{doc_id}_chk_{chunk_idx:03d}",
                "document_id": doc_id,
                "text": chunk_text,
                "content_hash": doc_hash,
                "metadata": {
                    "title": doc.get("title", ""),
                    "source": doc.get("source", ""),
                    "url": doc.get("url", ""),
                    "organization": doc.get("organization", ""),
                    "publication_date": doc.get("publication_date", ""),
                    "last_reviewed": doc.get("last_reviewed", ""),
                    "topic": doc.get("topic", ""),
                    "document_type": doc.get("document_type", ""),
                    "chunk_index": chunk_idx,
                },
            })
            chunk_idx += 1
            current_sentences = [sentence]
            current_len = sent_len
        else:
            current_sentences.append(sentence)
            current_len += sent_len + 1

    if current_sentences:
        chunk_text = " ".join(current_sentences)
        chunks.append({
            "chunk_id": f"{doc_id}_chk_{chunk_idx:03d}",
            "document_id": doc_id,
            "text": chunk_text,
            "content_hash": doc_hash,
            "metadata": {
                "title": doc.get("title", ""),
                "source": doc.get("source", ""),
                "url": doc.get("url", ""),
                "organization": doc.get("organization", ""),
                "publication_date": doc.get("publication_date", ""),
                "last_reviewed": doc.get("last_reviewed", ""),
                "topic": doc.get("topic", ""),
                "document_type": doc.get("document_type", ""),
                "chunk_index": chunk_idx,
            },
        })

    return chunks
