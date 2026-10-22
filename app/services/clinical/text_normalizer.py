"""
Clinical Text Normalizer.
Performs safe Unicode normalization, contraction expansion,
punctuation cleaning, and standard colloquialism normalization
while preserving clinical integrity.
"""

import re
import unicodedata
from typing import Dict

# Common English contractions and colloquial clinical phrasing
CONTRACTIONS_MAP: Dict[str, str] = {
    "can't": "cannot",
    "won't": "will not",
    "i've": "i have",
    "i'm": "i am",
    "i'd": "i would",
    "i'll": "i will",
    "he's": "he is",
    "she's": "she is",
    "it's": "it is",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "couldn't": "could not",
    "shouldn't": "should not",
    "wouldn't": "would not",
}


def normalize_unicode(text: str) -> str:
    """Normalize Unicode characters (NFKC) and replace smart quotes/dashes."""
    if not text:
        return ""
    # Normalize NFKC
    normalized = unicodedata.normalize("NFKC", text)
    # Smart quotes and apostrophes
    normalized = normalized.replace("‘", "'").replace("’", "'").replace("`", "'")
    normalized = normalized.replace("“", '"').replace("”", '"')
    # Em/en dashes to hyphen
    normalized = normalized.replace("—", "-").replace("–", "-")
    return normalized


def expand_contractions(text: str) -> str:
    """Expand common English contractions."""
    lower_text = text.lower()
    for contraction, expanded in CONTRACTIONS_MAP.items():
        # Match contraction with word boundaries or apostrophe
        pattern = r"\b" + re.escape(contraction) + r"\b"
        lower_text = re.sub(pattern, expanded, lower_text)
    return lower_text


def clean_clinical_text(text: str) -> str:
    """
    Standardizes input clinical text:
    - Unicode normalized
    - Contractions expanded
    - Extra whitespace collapsed
    """
    if not text:
        return ""
    text = normalize_unicode(text)
    text = expand_contractions(text)
    # Collapse multiple spaces and newlines
    text = re.sub(r"\s+", " ", text).strip()
    return text
