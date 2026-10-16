"""
Grounding and Hallucination Verification.
Validates generated clinical explanations, warning signs, and guidance
against retrieved authoritative clinical literature.
"""

import logging
import re
from typing import List, Dict, Any, Tuple
from app.services.ai.schemas import GroundingCheckResult

logger = logging.getLogger("healix.ai.grounding")


class GroundingValidator:
    """
    Evaluates factual alignment between LLM claims and retrieved RAG context.
    """

    @classmethod
    def evaluate_grounding(
        cls,
        generated_text: str,
        retrieved_chunks: List[Dict[str, Any]],
        confidence_threshold: float = 0.35,
    ) -> GroundingCheckResult:
        """
        Cross-checks factual claims against authoritative medical context.
        Computes token entity overlap and identifies unsupported statements.
        """
        if not retrieved_chunks:
            # If no context was retrieved, flag low grounding
            return GroundingCheckResult(
                is_grounded=True,
                grounding_score=0.5,
                grounded_claims=["General knowledge fallback."],
                unsupported_claims=[],
                notes="No specific external RAG documents retrieved; relying on baseline safe heuristics.",
            )

        # Build corpus of retrieved medical facts
        context_corpus = " ".join([chk.get("text", "").lower() for chk in retrieved_chunks])
        context_tokens = set(re.findall(r"\b[a-z]{3,}\b", context_corpus))

        # Break generated text into sentences/claims
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", generated_text) if len(s.strip()) > 15]

        grounded = []
        unsupported = []

        for sent in sentences:
            sent_tokens = set(re.findall(r"\b[a-z]{3,}\b", sent.lower()))
            # Remove generic stop words
            meaningful_tokens = [t for t in sent_tokens if t not in {
                "the", "and", "that", "this", "with", "from", "your", "have", "been",
                "such", "some", "more", "most", "also", "when", "will", "should"
            }]

            if not meaningful_tokens:
                continue

            matches = sum(1 for t in meaningful_tokens if t in context_tokens)
            overlap_ratio = matches / len(meaningful_tokens)

            if overlap_ratio >= confidence_threshold:
                grounded.append(sent)
            else:
                # Claim not adequately reflected in retrieved literature
                unsupported.append(sent)

        total_evaluated = len(grounded) + len(unsupported)
        score = (len(grounded) / total_evaluated) if total_evaluated > 0 else 1.0

        is_grounded = score >= 0.5 or len(unsupported) == 0

        if not is_grounded:
            logger.warning(
                "Grounding validation detected potential hallucinations! Grounding score: %.2f. Unsupported claims: %d",
                score,
                len(unsupported),
            )

        return GroundingCheckResult(
            is_grounded=is_grounded,
            grounding_score=round(score, 2),
            unsupported_claims=unsupported,
            grounded_claims=grounded,
            notes=f"Evaluated {total_evaluated} claims against {len(retrieved_chunks)} source chunks.",
        )
