import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_check_app_health(client):
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"message": "ITS ALIVE!!!"}

def test_storage_bucket_list(client):
    response = client.get("/storage/get-bucket-list/")
    assert response.status_code == 200

    bucket_ans = {
        "buckets": [
            "backstageil"
        ]
    }

    assert response.json() == bucket_ans


def test_db_first_element(client):
    response = client.get("/db/music-halls/1")
    assert response.status_code == 200

    hall_1 = {
        "city": "Tel Aviv",
        "hall_name": "Kameri 1",
        "email": "kameri@example.com",
        "stage": True,
        "pipe_height": 10,
        "stage_type": "raised"
    }
    assert response.json() == hall_1