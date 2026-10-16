"""
Follow-Up Question Engine.
Generates adaptive, clinically relevant, concise, and non-technical
intake questions based on presenting symptoms and user history.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from app.services.ai.llm.base import BaseLLMProvider
from app.services.ai.llm.provider import get_llm_provider
from app.services.ai.schemas import FollowUpQuestionsResponse, AIQuestionItem
from app.services.ai.prompts.follow_up import (
    FOLLOW_UP_SYSTEM_PROMPT,
    FOLLOW_UP_USER_PROMPT_TEMPLATE,
)

logger = logging.getLogger("healix.ai.follow_up")


class FollowUpQuestionEngine:
    """
    Generates dynamic follow-up intake questions tailored to reported symptoms.
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_llm_provider()

    async def generate_questions(
        self,
        description: str,
        symptoms: List[Dict[str, Any]],
        previous_answers: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generates 2 to 5 targeted follow-up questions.
        """
        previous_answers = previous_answers or []
        symptoms_json = json.dumps(symptoms, indent=2)
        answers_json = json.dumps(previous_answers, indent=2)

        prompt = FOLLOW_UP_USER_PROMPT_TEMPLATE.format(
            description=description or "No narrative provided",
            symptoms_json=symptoms_json,
            previous_answers_json=answers_json,
        )

        try:
            res: FollowUpQuestionsResponse = await self.llm.generate_structured(
                schema=FollowUpQuestionsResponse,
                prompt=prompt,
                system_prompt=FOLLOW_UP_SYSTEM_PROMPT,
                temperature=0.2,
            )
            questions = [
                {
                    "question": q.question,
                    "type": q.type,
                    "order_index": idx,
                    "reasoning": q.reasoning,
                    "options": q.options,
                }
                for idx, q in enumerate(res.questions)
            ]
            if questions:
                return questions
        except Exception as e:
            logger.warning("AI Follow-up question generation failed (%s). Using fallback questions.", str(e))

        return self._generate_fallback_questions(description, symptoms)

    def _generate_fallback_questions(
        self, description: str, symptoms: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        text = (description + " " + " ".join([s.get("name", "") for s in symptoms])).lower()

        if "head" in text:
            return [
                {
                    "question": "Did the headache begin suddenly like a clap of thunder, or develop slowly over time?",
                    "type": "single_choice",
                    "order_index": 0,
                    "reasoning": "Screen for sudden acute neurological emergencies.",
                    "options": ["Built up gradually", "Started over a few hours", "Sudden severe clap of thunder"],
                },
                {
                    "question": "How severe is the headache right now on a scale from 0 to 10?",
                    "type": "single_choice",
                    "order_index": 1,
                    "reasoning": "Assess pain severity.",
                    "options": ["1-3 (Mild)", "4-6 (Moderate)", "7-9 (Severe)", "10 (Worst headache of life)"],
                },
                {
                    "question": "Are you experiencing any neck stiffness, fever, or sensitivity to light?",
                    "type": "single_choice",
                    "order_index": 2,
                    "reasoning": "Identify possible meningeal irritation signs.",
                    "options": ["None of these", "Mild light sensitivity", "Stiff neck or fever"],
                },
            ]
        elif "chest" in text:
            return [
                {
                    "question": "Does the chest discomfort radiate to your left arm, shoulder, back, or jaw?",
                    "type": "single_choice",
                    "order_index": 0,
                    "reasoning": "Evaluate potential ischemic radiation.",
                    "options": ["No radiation", "Radiates to left arm or jaw", "Radiates to back"],
                },
                {
                    "question": "Are you also experiencing shortness of breath, nausea, or cold sweats?",
                    "type": "single_choice",
                    "order_index": 1,
                    "reasoning": "Screen for systemic cardiopulmonary indicators.",
                    "options": ["None of these", "Mild shortness of breath", "Sweating and significant breathlessness"],
                },
            ]
        else:
            return [
                {
                    "question": "How long have you been experiencing these symptoms?",
                    "type": "single_choice",
                    "order_index": 0,
                    "reasoning": "Establish chronological timeline.",
                    "options": ["Less than 24 hours", "1 to 3 days", "4 to 7 days", "More than a week"],
                },
                {
                    "question": "How would you describe the overall severity of your symptoms?",
                    "type": "single_choice",
                    "order_index": 1,
                    "reasoning": "Gauge subjective impact.",
                    "options": ["Mild (does not interrupt activities)", "Moderate (interferes with tasks)", "Severe (unable to do normal activities)"],
                },
            ]
