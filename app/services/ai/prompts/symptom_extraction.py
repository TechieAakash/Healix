"""
Symptom Extraction Prompts.
Instructs LLM to extract structured symptom entities without inferring unstated symptoms.
"""

from app.services.ai.prompts.system import HEALTHCARE_SYSTEM_PROMPT

EXTRACTION_SYSTEM_PROMPT = f"""{HEALTHCARE_SYSTEM_PROMPT}

TASK:
Extract structured clinical symptoms, anatomical locations, reported severities, timelines, and associated features from the patient's natural language input.

STRICT EXTRACTION RULES:
1. ONLY extract symptoms explicitly mentioned or unmistakably described.
2. Mark extraction_type as:
   - "explicit": directly stated by user
   - "inferred": directly derived from clear colloquial descriptors (e.g. "my head is pounding" -> headache)
   - "unknown": if ambiguous
3. DO NOT extrapolate or fabricate unmentioned symptoms.
4. Extract associated clinical features (e.g. photophobia, phonophobia, nausea, worsening with movement) into associated_features.
5. If severity or duration is not stated, mark as "unknown" or "unspecified".
"""

EXTRACTION_USER_PROMPT_TEMPLATE = """Patient Description:
<<<
{user_input}
>>>

Extract structured symptoms and associated features conforming strictly to the requested schema.
"""
