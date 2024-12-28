import unittest
from fastapi.testclient import TestClient
from app.main import app



class TestGetMusicHall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method runs once before all tests."""
        cls.client = TestClient(app)

    def test_read_main(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, World!"}

    def test_fetch_music_hall(self):
        hall_id = 1
        response = self.client.get(f"/music-halls/{hall_id}", headers={"Content-Type": "application/json"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["city"], "Tel Aviv")
        self.assertEqual(response.json()["email"], "kameri@example.com")

