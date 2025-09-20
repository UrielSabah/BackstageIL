import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestGetMusicHall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests."""
        cls.client = TestClient(app)

    def test_read_main(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "ITS ALIVE!!!"})

