import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base, get_db
from app.main import app
from app.core.security import create_access_token
from app.models.user import User
from app.core.security import get_password_hash

# Use an in-memory SQLite database for isolated test execution
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session) -> User:
    user = User(
        name="Test Patient",
        email="patient@healix.com",
        password_hash=get_password_hash("SecurePassword123!"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def other_user(db_session) -> User:
    user = User(
        name="Other Patient",
        email="other@healix.com",
        password_hash=get_password_hash("SecurePassword123!"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(test_user) -> dict:
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def other_auth_headers(other_user) -> dict:
    token = create_access_token(other_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def hermetic_test_ai_provider(monkeypatch):
    """Exercise the real offline provider without external API dependencies."""
    from app.core.config import settings
    monkeypatch.setattr(settings, "AI_PROVIDER", "local")
