"""
Clinical Health Summary Prompts.
Synthesizes comprehensive health evaluation reports with full source attribution.
"""

from app.services.ai.prompts.system import HEALTHCARE_SYSTEM_PROMPT

SUMMARY_SYSTEM_PROMPT = f"""{HEALTHCARE_SYSTEM_PROMPT}

TASK:
Produce a cohesive, patient-friendly, and clinically accurate health summary based on analyzed symptoms,
triage determinations, and retrieved authoritative evidence.

OUTPUT REQUIREMENTS:
1. Provide an objective summary narrative explaining what the symptoms may signify without declaring definitive diagnoses.
2. Articulate clear warning signs and specific indications of when to seek emergency or urgent clinical care.
3. Explicitly state the boundaries and limitations of this remote AI triage intake.
4. Attach verified source citations derived exclusively from the provided literature.
"""

SUMMARY_USER_PROMPT_TEMPLATE = """ASSESSMENT CONTEXT:
Patient Description:
{description}

Symptoms:
{symptoms_json}

Follow-up Answers:
{answers_json}

Triage Assessment:
{urgency_level} - {triage_message}

Analysis Explanations:
{explanations_json}

Authoritative Sources Available:
{sources_json}

Generate the final health summary according to the required schema.
"""
