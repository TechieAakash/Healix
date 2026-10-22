import socket

import pytest

from app.services.ai.llm.local_provider import LocalLLMProvider
from app.services.ai.prompts.follow_up import FOLLOW_UP_USER_PROMPT_TEMPLATE
from app.services.ai.prompts.symptom_analysis import ANALYSIS_USER_PROMPT_TEMPLATE
from app.services.ai.schemas import FollowUpQuestionsResponse, SymptomAnalysisResponse, SymptomExtractionResponse
from app.services.triage_service import TriageService
from app.core.config import Settings


@pytest.mark.parametrize("description,expected", [
    ("I have a headache for 3 days", "headache"),
    ("My stomach hurts since yesterday", "abdominal pain"),
    ("I have a fever", "fever"),
    ("I keep coughing", "cough"),
    ("My throat is sore", "sore throat"),
    ("I feel nauseous", "nausea"),
    ("I have diarrhea", "diarrhea"),
    ("My lower back hurts", "back pain"),
    ("I feel dizzy", "dizziness"),
    ("I feel exhausted", "fatigue"),
])
@pytest.mark.asyncio
async def test_local_extraction_handles_common_symptoms(description, expected, monkeypatch):
    monkeypatch.setattr(socket, "socket", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network used")))
    prompt = f"Patient Description:\n{description}\n\nIdentified Symptoms:\n[]"
    result = await LocalLLMProvider().generate_structured(SymptomExtractionResponse, prompt)
    assert expected in {item.name for item in result.symptoms}


@pytest.mark.asyncio
async def test_local_followups_and_analysis_have_retrieval_citations():
    provider = LocalLLMProvider()
    followup_prompt = FOLLOW_UP_USER_PROMPT_TEMPLATE.format(
        description="I have a headache",
        symptoms_json='[{"name": "headache"}]',
        previous_answers_json="[]",
    )
    questions = await provider.generate_structured(FollowUpQuestionsResponse, followup_prompt)
    assert 1 <= len(questions.questions) <= 5

    from app.services.ai.rag.retriever import RAGRetriever
    retriever = RAGRetriever()
    chunks = await retriever.retrieve_context("headache and light sensitivity")
    context = retriever.build_rag_context_block(chunks)
    prompt = ANALYSIS_USER_PROMPT_TEMPLATE.format(
        description="I have a headache and light sensitivity",
        symptoms_json='[{"name": "headache"}]',
        answers_json="[]",
        urgency_level="ROUTINE",
        rag_context=context,
    )
    analysis = await provider.generate_structured(SymptomAnalysisResponse, prompt)
    assert analysis.possible_explanations
    assert all(item.sources for item in analysis.possible_explanations)


@pytest.mark.asyncio
async def test_local_chat_refuses_dosage_request():
    response = await LocalLLMProvider().generate_text("CURRENT USER QUERY:\n<<<\nHow many mg should I take?\n>>>")
    assert "can’t recommend" in response.text.lower()


def test_local_configuration_needs_no_api_key():
    local = Settings(_env_file=None, AI_PROVIDER="local", AI_API_KEY="")
    assert local.AI_PROVIDER == "local"
    with pytest.raises(ValueError, match="AI_API_KEY is required"):
        Settings(_env_file=None, AI_PROVIDER="openai", AI_API_KEY="")


@pytest.mark.asyncio
async def test_local_chat_includes_retrieved_citation():
    from app.services.ai.rag.retriever import RAGRetriever
    retriever = RAGRetriever()
    chunks = await retriever.retrieve_context("What can cause a headache?", top_k=2)
    prompt = (
        "ACTIVE ASSESSMENT CONTEXT (IF APPLICABLE):\nNo active assessment attached.\n\n"
        "RETRIEVED CLINICAL KNOWLEDGE:\n" + retriever.build_rag_context_block(chunks)
        + "\n\nCONVERSATION HISTORY:\n\nCURRENT USER QUERY:\n<<<\nWhat can cause a headache?\n>>>"
    )
    reply = await LocalLLMProvider().generate_text(prompt)
    assert "Source:" in reply.text
    assert "https://" in reply.text


@pytest.mark.parametrize("text", [
    "I have chest pain and pressure",
    "My face is drooping and speech is slurred",
])
def test_red_flag_phrases_force_emergency(text):
    assert TriageService().evaluate(text)["urgency_level"] == "EMERGENCY"
