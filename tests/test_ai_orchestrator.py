"""
Unit & Integration Tests for AI Orchestrator.
Tests end-to-end symptom extraction, adaptive questions, RAG context injection,
structured output generation, and source attribution.
"""

import pytest
from app.services.ai.orchestrator import AIOrchestrator
from app.services.ai.llm.provider import MockLLMProvider
from app.utils.constants import UrgencyLevel, STANDARD_MEDICAL_DISCLAIMER


@pytest.fixture
def orchestrator():
    return AIOrchestrator(llm_provider=MockLLMProvider())


@pytest.mark.asyncio
async def test_symptom_extraction_and_normalization(orchestrator):
    text = "I've had a headache on the right side since yesterday. It gets worse when I look at bright lights and I feel slightly nauseous."
    result = await orchestrator.extract_symptoms(text)

    assert result["original_text"] == text
    assert len(result["normalized_symptoms"]) >= 2
    symptom_names = [s["name"] for s in result["normalized_symptoms"]]
    assert "headache" in symptom_names
    assert "nausea" in symptom_names
    assert len(result["associated_features"]) > 0


@pytest.mark.asyncio
async def test_follow_up_questions_generation(orchestrator):
    description = "I've had a dull headache for two days"
    symptoms = [{"name": "headache", "severity": 4, "description": "dull band"}]

    questions = await orchestrator.generate_follow_up_questions(description, symptoms)
    assert len(questions) > 0
    assert len(questions) <= 7  # Maximum limit enforced
    for q in questions:
        assert "question" in q
        assert "type" in q
        assert len(q["question"]) > 10


@pytest.mark.asyncio
async def test_generate_summary_routine(orchestrator):
    description = "Mild temple tension after long computer work."
    symptoms = [{"name": "headache", "severity": 3, "description": "mild"}]
    answers = [{"question": "Did it start suddenly?", "answer": "No, gradually"}]
    triage_result = {
        "urgency_level": UrgencyLevel.ROUTINE.value,
        "message": "Symptoms appear routine.",
    }

    report = await orchestrator.generate_summary(
        description=description,
        symptoms=symptoms,
        answers=answers,
        triage_result=triage_result,
    )

    assert report["urgency_level"] == UrgencyLevel.ROUTINE.value
    assert len(report["possible_explanations"]) > 0
    assert len(report["sources"]) > 0
    assert report["disclaimer"] == STANDARD_MEDICAL_DISCLAIMER
    # Must preserve sources with title and organization
    for src in report["sources"]:
        assert "title" in src
        assert "organization" in src


@pytest.mark.asyncio
async def test_chat_dialogue_with_context(orchestrator):
    history = [
        {"role": "user", "content": "I have had a mild headache since yesterday."},
        {"role": "assistant", "content": "Rest and hydration can often assist."},
    ]
    reply = await orchestrator.chat(
        user_message="Could mild dehydration cause this headache?",
        conversation_history=history,
    )
    assert len(reply) > 20
    assert "dehydration" in reply.lower()
    # Must include medical disclaimer
    assert "medical diagnosis" in reply.lower() or "healix" in reply.lower()
