"""
Negation and Context Detector for Clinical Symptom Screening.
Detects whether a symptom concept in text is explicitly negated,
hypothetical, or refers to a third party (e.g. family member/friend),
preventing false emergency triggers on phrases like "no chest pain".
"""

import re
from typing import List, Tuple, Optional

# Regular expressions for negation cues
PRE_NEGATION_PATTERNS = [
    r"\b(?:no|not|none|never|without|denies|denied|denying)\b",
    r"\b(?:negative for|free of|rules out|ruled out|r/o)\b",
    r"\b(?:did not have|does not have|do not have|have not had|has not had|haven't had|hasn't had)\b",
    r"\b(?:no sign of|no evidence of|no history of)\b",
    r"\b(?:zero|neither|nor)\b",
]

POST_NEGATION_PATTERNS = [
    r"\b(?:is ruled out|was ruled out|is absent|was absent|has resolved|is negative)\b",
    r"\b(?:not present|not observed|unlikely)\b",
]

# Non-patient context cues (family, friends, general hypothetical questions)
THIRD_PARTY_OR_HYPOTHETICAL_PATTERNS = [
    r"\b(?:my\s+(?:mom|mother|dad|father|friend|colleague|coworker|brother|sister|wife|husband|partner|son|daughter|child|kid|neighbor))\b",
    r"\b(?:someone|anyone|people)\b",
    r"\b(?:what if|could it be|is it possible|wondering if|hypothetically|does\s+(?:having)?|what does)\b",
]

# Conjunctions that terminate a negation scope within a sentence
CONTRASTIVE_CONJUNCTIONS = [
    r"\b(?:but|however|although|except|yet|nevertheless|though)\b",
]


class NegationDetector:
    """
    Clause-aware clinical negation and context evaluator.
    """

    def __init__(self):
        self.pre_neg_re = re.compile("|".join(PRE_NEGATION_PATTERNS), re.IGNORECASE)
        self.post_neg_re = re.compile("|".join(POST_NEGATION_PATTERNS), re.IGNORECASE)
        self.third_party_re = re.compile("|".join(THIRD_PARTY_OR_HYPOTHETICAL_PATTERNS), re.IGNORECASE)
        self.contrastive_re = re.compile("|".join(CONTRASTIVE_CONJUNCTIONS), re.IGNORECASE)

    def split_into_clauses(self, text: str) -> List[str]:
        """Split text into manageable grammatical clauses bounded by punctuation or contrast."""
        # Split on sentence boundaries and punctuation
        raw_clauses = re.split(r"[.;:\n\r]+", text)
        result = []
        for c in raw_clauses:
            c = c.strip()
            if not c:
                continue
            # Further split by contrastive conjunctions (e.g., "no fever but severe headache")
            sub_clauses = self.contrastive_re.split(c)
            for sub in sub_clauses:
                sub_clean = sub.strip()
                if sub_clean:
                    result.append(sub_clean)
        return result

    def is_negated(self, phrase: str, clause: str, max_word_distance: int = 5) -> bool:
        """
        Check if `phrase` is preceded by a pre-negation cue or followed by a post-negation cue
        within `max_word_distance` words inside the same clause.
        """
        clause_lower = clause.lower()
        phrase_lower = phrase.lower()

        # Find position of phrase
        match = re.search(r"\b" + re.escape(phrase_lower) + r"\b", clause_lower)
        if not match:
            # Fallback to direct substring search if word boundary fails
            idx = clause_lower.find(phrase_lower)
            if idx == -1:
                return False
            start_pos, end_pos = idx, idx + len(phrase_lower)
        else:
            start_pos, end_pos = match.start(), match.end()

        # Preceding text window
        pre_text = clause_lower[:start_pos].strip()
        pre_words = pre_text.split()[-max_word_distance:] if pre_text else []
        pre_window = " ".join(pre_words)

        if pre_window and self.pre_neg_re.search(pre_window):
            return True

        # Following text window
        post_text = clause_lower[end_pos:].strip()
        post_words = post_text.split()[:max_word_distance] if post_text else []
        post_window = " ".join(post_words)

        if post_window and self.post_neg_re.search(post_window):
            return True

        return False

    def is_third_party_or_hypothetical(self, phrase: str, clause: str) -> bool:
        """Check if the phrase appears in a hypothetical or third-party context."""
        clause_lower = clause.lower()
        return bool(self.third_party_re.search(clause_lower))


negation_detector = NegationDetector()
