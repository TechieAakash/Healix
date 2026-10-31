import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import init_db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_db()

@pytest.mark.asyncio
async def test_full_api_integration():
    test_email = f"tester_{uuid.uuid4().hex[:8]}@healix.ai"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Health check
        res = await ac.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"

        # 2. Register new user
        reg_payload = {
            "email": test_email,
            "password": "Password123!#",
            "full_name": "Integration Tester",
            "date_of_birth": "1998-05-20",
            "biological_sex": "OTHER",
            "clinical_consent_acknowledged": True
        }
        reg_res = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert reg_res.status_code == 200
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Get profile /auth/me
        me_res = await ac.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == test_email

        # 4. Test Symptom Catalog API
        catalog_res = await ac.get("/api/v1/symptoms/catalog")
        assert catalog_res.status_code == 200
        cat_data = catalog_res.json()
        assert cat_data["total_symptoms"] > 10
        assert len(cat_data["anatomical_locations"]) > 5

        # 5. Test Natural Language Symptom Parsing API
        parse_res = await ac.post(
            "/api/v1/symptoms/parse",
            json={"free_text": "I have had a throbbing headache on my right temple for two days with nausea, but no fever."}
        )
        assert parse_res.status_code == 200
        parsed = parse_res.json()
        assert "sym_headache" in parsed["extracted_symptom_ids"]
        assert "symptom.fever" in parsed["negated_facts"]

        # 6. Start Multi-Step Assessment
        start_payload = {
            "primary_complaint": "Right temporal throbbing headache with nausea",
            "symptom_ids": parsed["extracted_symptom_ids"],
            "location_ids": ["loc_temple_right"],
            "duration": "1-3 Days",
            "severity": "Moderate",
            "character": "Pulsating / Throbbing"
        }
        start_res = await ac.post("/api/v1/assessments/start", headers=headers, json=start_payload)
        assert start_res.status_code == 201
        aid = start_res.json()["assessment_id"]

        # 7. Adaptive Questions: Answer critical clarifying questions (thunderclap, neuro deficits, neck stiffness)
        for _ in range(4):
            q_res = await ac.get(f"/api/v1/assessments/{aid}/next-question", headers=headers)
            assert q_res.status_code == 200
            q_data = q_res.json()
            if not q_data.get("has_more_questions") or not q_data.get("question"):
                break
            q = q_data["question"]
            ans_payload = {
                "question_id": q["id"],
                "fact_name": q["target_fact_name"],
                "value": "FALSE"
            }
            ans_res = await ac.post(f"/api/v1/assessments/{aid}/answer", headers=headers, json=ans_payload)
            assert ans_res.status_code == 200

        # 9. Complete Assessment
        comp_res = await ac.post(f"/api/v1/assessments/{aid}/complete", headers=headers)
        assert comp_res.status_code == 200
        comp_data = comp_res.json()
        assert comp_data["status"] == "COMPLETED"
        assert "narrative" in comp_data
        assert len(comp_data["conclusions"]) > 0

        # 10. Generate Report
        rep_res = await ac.post(f"/api/v1/assessments/{aid}/reports", headers=headers)
        assert rep_res.status_code == 200
        assert "checksum_sha256" in rep_res.json()

        # 11. Verify Timeline Record Created
        time_res = await ac.get("/api/v1/timeline", headers=headers)
        assert time_res.status_code == 200
        assert len(time_res.json()) >= 1
