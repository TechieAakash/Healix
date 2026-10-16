def test_create_symptom_success(client, auth_headers):
    response = client.post(
        "/api/v1/symptoms",
        headers=auth_headers,
        json={
            "name": "Headache",
            "description": "Pain around forehead and temples",
            "severity": 6,
            "body_location": "forehead",
            "duration": "2 days",
            "frequency": "constant",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Headache"
    assert data["severity"] == 6


def test_create_symptom_invalid_severity(client, auth_headers):
    # Severity > 10 should fail validation
    response = client.post(
        "/api/v1/symptoms",
        headers=auth_headers,
        json={"name": "Extreme Pain", "severity": 15},
    )
    assert response.status_code in [400, 422]


def test_list_user_symptoms(client, auth_headers):
    # Create two symptoms
    client.post("/api/v1/symptoms", headers=auth_headers, json={"name": "Cough", "severity": 3})
    client.post("/api/v1/symptoms", headers=auth_headers, json={"name": "Fatigue", "severity": 4})

    response = client.get("/api/v1/symptoms", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["total"] >= 2


def test_symptom_ownership_idor_protection(client, auth_headers, other_auth_headers):
    # User 1 creates symptom
    create_res = client.post(
        "/api/v1/symptoms",
        headers=auth_headers,
        json={"name": "Confidential Symptom", "severity": 5},
    )
    symptom_id = create_res.json()["id"]

    # User 2 attempts to read User 1's symptom
    get_res = client.get(f"/api/v1/symptoms/{symptom_id}", headers=other_auth_headers)
    assert get_res.status_code == 404 # Concealed as 404 to avoid information disclosure


def test_delete_symptom(client, auth_headers):
    create_res = client.post(
        "/api/v1/symptoms",
        headers=auth_headers,
        json={"name": "Transient Rash", "severity": 2},
    )
    symptom_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/symptoms/{symptom_id}", headers=auth_headers)
    assert del_res.status_code == 200

    # Ensure it's deleted
    get_res = client.get(f"/api/v1/symptoms/{symptom_id}", headers=auth_headers)
    assert get_res.status_code == 404
