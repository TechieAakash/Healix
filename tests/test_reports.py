def test_report_generation_and_retrieval(client, auth_headers):
    # Create symptom and assessment
    symptom_res = client.post(
        "/api/v1/symptoms",
        headers=auth_headers,
        json={"name": "Sinus Pressure", "severity": 4},
    )
    s_id = symptom_res.json()["id"]

    init_res = client.post(
        "/api/v1/assessments",
        headers=auth_headers,
        json={"description": "Sinus congestion and pressure", "symptoms": [s_id]},
    )
    a_id = init_res.json()["assessment_id"]

    # Generate report directly
    gen_res = client.post(f"/api/v1/reports/{a_id}/generate", headers=auth_headers)
    assert gen_res.status_code == 201
    report_data = gen_res.json()
    assert report_data["assessment_id"] == a_id
    assert "possible_explanations" in report_data

    # List reports
    list_res = client.get("/api/v1/reports", headers=auth_headers)
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # Fetch specific report
    report_id = report_data["id"]
    fetch_res = client.get(f"/api/v1/reports/{report_id}", headers=auth_headers)
    assert fetch_res.status_code == 200
    assert fetch_res.json()["id"] == report_id


def test_chat_dialogue_workflow(client, auth_headers):
    # 1. Create conversation session
    create_res = client.post(
        "/api/v1/chat/conversations",
        headers=auth_headers,
        json={"title": "Headache Inquiry"},
    )
    assert create_res.status_code == 201
    conv_id = create_res.json()["id"]

    # 2. Post a message to AI assistant
    msg_res = client.post(
        f"/api/v1/chat/conversations/{conv_id}/messages",
        headers=auth_headers,
        json={"message": "Could dehydration cause my tension headache?"},
    )
    assert msg_res.status_code == 201
    msg_data = msg_res.json()
    assert msg_data["role"] == "ASSISTANT"
    assert "dehydration" in msg_data["content"].lower()

    # 3. Retrieve conversation history
    history_res = client.get(
        f"/api/v1/chat/conversations/{conv_id}",
        headers=auth_headers,
    )
    assert history_res.status_code == 200
    messages = history_res.json()["messages"]
    assert len(messages) >= 2 # 1 User message + 1 Assistant response
