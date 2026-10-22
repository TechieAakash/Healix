def test_create_assessment_workflow(client, auth_headers):
    # 1. Create a symptom
    symptom_res = client.post(
        "/api/v1/symptoms",
        headers=auth_headers,
        json={"name": "Headache", "severity": 4, "description": "Dull ache"},
    )
    symptom_id = symptom_res.json()["id"]

    # 2. Initialize assessment
    init_res = client.post(
        "/api/v1/assessments",
        headers=auth_headers,
        json={
            "description": "I've had a headache since yesterday",
            "symptoms": [symptom_id],
        },
    )
    assert init_res.status_code == 201
    assessment_id = init_res.json()["assessment_id"]
    assert init_res.json()["status"] == "SYMPTOMS_COLLECTED"

    # 3. Request follow-up questions
    questions_res = client.post(
        f"/api/v1/assessments/{assessment_id}/questions",
        headers=auth_headers,
    )
    assert questions_res.status_code == 200
    questions = questions_res.json()["questions"]
    assert len(questions) > 0
    first_q = questions[0]
    assert first_q["reasoning"]
    if first_q.get("evidence_code"):
        assert first_q["options"] == ["Yes", "No", "Not sure"]

    # 4. Submit an answer
    answer_res = client.post(
        f"/api/v1/assessments/{assessment_id}/answers",
        headers=auth_headers,
        json={"question_id": first_q["id"], "answer": "No"},
    )
    assert answer_res.status_code == 201

    # 5. Run triage analysis
    analyze_res = client.post(
        f"/api/v1/assessments/{assessment_id}/analyze",
        headers=auth_headers,
    )
    assert analyze_res.status_code == 200
    data = analyze_res.json()
    assert data["assessment_id"] == assessment_id
    assert "urgency_level" in data
    assert "summary" in data
    # Findings are grounded educational references, not diagnoses.
    assert data["possible_explanations"]
    assert all(item["sources"] for item in data["possible_explanations"])
    assert data["sources"]
    assert "disclaimer" in data
    assert "reasoning_trace" in data

    assessment_res = client.get(f"/api/v1/assessments/{assessment_id}", headers=auth_headers)
    assert assessment_res.status_code == 200
    assert assessment_res.json()["status"] == "COMPLETED"
    assert assessment_res.json()["report"] is not None


def test_emergency_rule_trace_is_returned_and_persisted(client, auth_headers):
    init_res = client.post(
        "/api/v1/assessments",
        headers=auth_headers,
        json={"description": "I have severe chest pain radiating to my arm"},
    )
    assessment_id = init_res.json()["assessment_id"]

    analyze_res = client.post(f"/api/v1/assessments/{assessment_id}/analyze", headers=auth_headers)
    assert analyze_res.status_code == 200
    data = analyze_res.json()
    assert data["urgency_level"] == "EMERGENCY"
    assert data["reasoning_trace"][0]["rule_id"] == "RULE_CARDIO_001"
    assert data["condition_ranking"] == []

    assessment_res = client.get(f"/api/v1/assessments/{assessment_id}", headers=auth_headers)
    trace = assessment_res.json()["report"]["reasoning_trace"]
    assert trace[0]["rule_id"] == "RULE_CARDIO_001"


def test_follow_up_answers_advance_to_a_new_dataset_question(client, auth_headers):
    init = client.post(
        "/api/v1/assessments",
        headers=auth_headers,
        json={"description": "I have a fever, cough, and sore throat"},
    )
    assessment_id = init.json()["assessment_id"]
    first_response = client.post(f"/api/v1/assessments/{assessment_id}/questions", headers=auth_headers)
    first = first_response.json()["questions"]
    assert first
    pending = first
    seen_question_ids = set()
    dataset_question = None
    for _ in range(5):
        question = pending[0]
        assert question["id"] not in seen_question_ids
        seen_question_ids.add(question["id"])
        if question.get("evidence_code"):
            dataset_question = question
            break
        answered = client.post(
            f"/api/v1/assessments/{assessment_id}/answers",
            headers=auth_headers,
            json={"question_id": question["id"], "answer": "No"},
        )
        assert answered.status_code == 201
        next_response = client.post(f"/api/v1/assessments/{assessment_id}/questions", headers=auth_headers)
        pending = next_response.json()["questions"]
        assert pending
    assert dataset_question
    assert dataset_question["options"] == ["Yes", "No", "Not sure"]


def test_assessment_ownership_idor(client, auth_headers, other_auth_headers):
    # User 1 initializes assessment
    init_res = client.post(
        "/api/v1/assessments",
        headers=auth_headers,
        json={"description": "Private Assessment"},
    )
    assessment_id = init_res.json()["assessment_id"]

    # User 2 attempts to fetch User 1's assessment
    fetch_res = client.get(
        f"/api/v1/assessments/{assessment_id}",
        headers=other_auth_headers,
    )
    assert fetch_res.status_code == 404


def test_assessment_failure_recovery(client, auth_headers, monkeypatch):
    """Verify that if analysis encounters an error, state is set to FAILED and can be recovered."""
    import app.services.ai_service as ai_service

    init_res = client.post(
        "/api/v1/assessments",
        headers=auth_headers,
        json={"description": "Test failure recovery"},
    )
    assessment_id = init_res.json()["assessment_id"]

    class BrokenAIService:
        async def generate_summary(self, **kwargs):
            raise RuntimeError("Simulated transient analysis failure")

    monkeypatch.setattr(ai_service, "get_ai_service", lambda: BrokenAIService())

    # Call analyze endpoint -> should fail
    analyze_res = client.post(
        f"/api/v1/assessments/{assessment_id}/analyze",
        headers=auth_headers,
    )
    assert analyze_res.status_code == 500

    # Fetch assessment details: status must be FAILED, NOT stuck in ANALYZING!
    fetch_res = client.get(
        f"/api/v1/assessments/{assessment_id}",
        headers=auth_headers,
    )
    assert fetch_res.status_code == 200
    assert fetch_res.json()["status"] == "FAILED"
