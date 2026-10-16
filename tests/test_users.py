def test_get_current_user_profile(client, auth_headers, test_user):
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name


def test_update_current_user_profile(client, auth_headers):
    response = client.patch(
        "/api/v1/users/me",
        headers=auth_headers,
        json={"name": "Aakash Updated", "gender": "Male"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Aakash Updated"


def test_purge_user_health_data(client, auth_headers):
    response = client.delete("/api/v1/users/me/data", headers=auth_headers)
    assert response.status_code == 200
    assert "wiped" in response.json()["message"].lower()


def test_delete_user_account(client, auth_headers, test_user):
    response = client.delete("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200

    # User should no longer be able to log in or access /me
    retry_response = client.get("/api/v1/users/me", headers=auth_headers)
    assert retry_response.status_code == 401
