"""
Adaptive Follow-up Question Prompts.
Instructs AI to generate targeted, clinically informative, short,
and non-technical questions based on symptoms and previous answers.
"""

from app.services.ai.prompts.system import HEALTHCARE_SYSTEM_PROMPT

FOLLOW_UP_SYSTEM_PROMPT = f"""{HEALTHCARE_SYSTEM_PROMPT}

TASK:
Generate targeted, clinical follow-up questions to clarify patient symptoms, progression, and safety status.

GUIDELINES FOR QUESTIONS:
1. SHORT & NON-TECHNICAL:
   - Use plain, conversational language understandable to an everyday patient.
   - Example: "How severe is the pain on a scale from 0 to 10?" NOT "Please quantify the intensity of your cephalalgia."
2. HIGH CLINICAL VALUE:
   - Only ask questions that materially clarify symptom severity, acute red-flag risks, or clinical timeline.
   - Avoid trivial, redundant, or repetitive inquiries.
3. ADAPTIVE:
   - Factor in any previous answers provided by the user. If the user already answered a detail, do NOT ask it again.
   - Focus questions according to the anatomical site and symptom evolution.
4. STRICT LIMIT:
   - Generate between 2 and 5 highly focused questions (MAXIMUM 7).
"""

FOLLOW_UP_USER_PROMPT_TEMPLATE = """Patient Description:
{description}

Identified Symptoms:
{symptoms_json}

Previous Answers (if any):
{previous_answers_json}

Generate focused follow-up questions in the required schema to clarify severity, timeline, and rule out red flags.
"""
