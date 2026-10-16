"""
PII, Sensitive Data, and Prompt Injection Sanitizer.
Sanitizes patient queries, removes sensitive identifiers (emails, phone numbers,
tokens, passwords), and neutralizes prompt injection payloads before forwarding to LLM.
"""

import re
from typing import Dict, Any, List

# Regular expressions for common PII patterns
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
SSN_REGEX = r"\b\d{3}-\d{2}-\d{4}\b"
BEARER_TOKEN_REGEX = r"Bearer\s+[A-Za-z0-9\-._~+/]+=*"
GENERIC_KEY_REGEX = r"(?:api[_-]?key|secret|token|password)[\s:=]+['\"]?([A-Za-z0-9_\-]{16,})['\"]?"

# Common adversarial jailbreak / prompt injection markers
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior|system)\s+instructions",
    r"you\s+are\s+now\s+(in\s+developer\s+mode|dan|jailbroken|unfiltered)",
    r"system\s*override",
    r"forget\s+that\s+you\s+are\s+(a\s+doctor|healix|an\s+ai)",
    r"act\s+as\s+a\s+licensed\s+physician\s+and\s+diagnose",
    r"prescribe\s+me\s+medication",
    r"tell\s+me\s+to\s+stop\s+taking\s+my\s+prescribed",
]


class ContextSanitizer:
    """
    Sanitizes patient inputs and contextual payloads prior to AI ingestion.
    """

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """
        Strips emails, phones, SSNs, and api tokens from patient narrative.
        """
        if not text:
            return ""

        sanitized = text
        sanitized = re.sub(EMAIL_REGEX, "[REDACTED_EMAIL]", sanitized)
        sanitized = re.sub(PHONE_REGEX, "[REDACTED_PHONE]", sanitized)
        sanitized = re.sub(SSN_REGEX, "[REDACTED_ID]", sanitized)
        sanitized = re.sub(BEARER_TOKEN_REGEX, "[REDACTED_TOKEN]", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(GENERIC_KEY_REGEX, "key=[REDACTED]", sanitized, flags=re.IGNORECASE)

        return sanitized.strip()

    @classmethod
    def inspect_and_neutralize_prompt_injection(cls, text: str) -> str:
        """
        Detects prompt injection triggers and defuses adversarial instruction overrides.
        """
        sanitized = text
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                # Neutralize injection by escaping and appending safety guard note
                sanitized = re.sub(
                    pattern,
                    "[BLOCKED_ADVERSARIAL_INSTRUCTION]",
                    sanitized,
                    flags=re.IGNORECASE,
                )

        return sanitized

    @classmethod
    def sanitize_context_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deeply cleans dictionary context passed to LLM prompts, ensuring
        no internal tokens, password hashes, or full sensitive profiles are exposed.
        """
        clean_dict = {}
        disallowed_keys = {
            "password", "password_hash", "hashed_password", "token",
            "access_token", "refresh_token", "jwt", "secret", "user_id"
        }

        for k, v in data.items():
            if k.lower() in disallowed_keys:
                continue
            if isinstance(v, str):
                clean_dict[k] = cls.sanitize_text(v)
            elif isinstance(v, list):
                clean_dict[k] = [
                    cls.sanitize_text(item) if isinstance(item, str) else item
                    for item in v
                ]
            else:
                clean_dict[k] = v

        return clean_dict
