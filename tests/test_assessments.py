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
    assert len(data["possible_explanations"]) > 0
    assert len(data["sources"]) > 0
    assert "disclaimer" in data


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
