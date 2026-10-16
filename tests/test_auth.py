def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Aakash Sharma",
            "email": "aakash.new@healix.com",
            "password": "StrongPassword123!",
            "gender": "Male",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Aakash Sharma"
    assert data["email"] == "aakash.new@healix.com"
    assert "password_hash" not in data


def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Duplicate User",
            "email": test_user.email,
            "password": "StrongPassword123!",
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "USER_ALREADY_EXISTS"


def test_register_weak_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Weak User",
            "email": "weak@healix.com",
            "password": "short",
        },
    )
    assert response.status_code in [400, 422]


def test_login_success(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "patient@healix.com",
            "password": "SecurePassword123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "patient@healix.com",
            "password": "WrongPassword123!",
        },
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_protected_route_without_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code in [401, 403]


def test_protected_route_with_token(client, auth_headers, test_user):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
