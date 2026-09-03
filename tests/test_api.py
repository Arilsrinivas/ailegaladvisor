import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from fastapi.testclient import TestClient
from src.api.main import app

class TestLegalAdvisorAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_system_stats(self):
        response = self.client.get("/api/compliance/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "HEALTHY")
        self.assertGreaterEqual(data["authoritative_sources_count"], 20)

    def test_precedents_search(self):
        response = self.client.get("/api/precedents/search?q=theft")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertGreater(len(results), 0)
        self.assertTrue(any("303" in r["title"] or "Theft" in r["title"] for r in results))

    def test_qa_query_english(self):
        response = self.client.post("/api/qa/query", json={
            "query": "What is the punishment for theft under the new BNS code?"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["detected_language"], "en")
        self.assertTrue("Section 303" in data["answer"] or "theft" in data["answer"].lower())
        self.assertGreater(len(data["retrieved_sources"]), 0)
        self.assertGreater(len(data["citations"]), 0)

    def test_qa_query_hindi(self):
        response = self.client.post("/api/qa/query", json={
            "query": "चोरी की सजा क्या है?"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["detected_language"], "hi")
        self.assertGreater(len(data["retrieved_sources"]), 0)

    def test_citation_verification(self):
        sample_text = "According to BNS Section 303, whoever commits theft shall be punished with imprisonment up to 3 years. Under IPC Section 302, punishment for murder is death."
        response = self.client.post("/api/citations/verify", json={"text": sample_text})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(data["total_citations"], 2)
        verifications = data["verifications"]
        replaced = [v for v in verifications if v["status"] == "REPLACED_BY_NEW_CODE"]
        self.assertGreater(len(replaced), 0)

    def test_legal_drafting(self):
        templates_res = self.client.get("/api/drafts/templates")
        self.assertEqual(templates_res.status_code, 200)
        templates = templates_res.json()
        self.assertGreaterEqual(len(templates), 5)

        draft_res = self.client.post("/api/drafts/generate", json={
            "template_type": "regular_bail",
            "form_data": {
                "applicant_name": "Ravi Kumar",
                "fir_no": "99/2026",
                "police_station": "Connaught Place",
                "sections": "BNS Section 303"
            }
        })
        self.assertEqual(draft_res.status_code, 200)
        draft = draft_res.json()
        self.assertIn("APPLICATION UNDER SECTION 480", draft["generated_content"])
        self.assertIn("Ravi Kumar", draft["generated_content"])

    def test_outcome_prediction(self):
        response = self.client.post("/api/outcomes/predict", json={
            "case_title": "State v. Ramesh",
            "offence_name": "Theft",
            "applied_sections": ["BNS Section 303"],
            "max_punishment_years": 3,
            "is_first_offender": True,
            "days_in_custody": 120,
            "flight_risk": "low"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(data["probability_score"], 60.0)
        self.assertGreater(len(data["favorable_factors"]), 0)
        self.assertGreater(len(data["guidelines_applied"]), 0)

if __name__ == "__main__":
    unittest.main()
