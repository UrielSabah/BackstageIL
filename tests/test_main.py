import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.db.neondb import init_db, close_db


@pytest_asyncio.fixture
async def client():
    """Async HTTP client with app lifespan (DB init/close) so DB-dependent tests work."""
    await init_db(app)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
    finally:
        await close_db(app)


@pytest.mark.asyncio
async def test_check_app_health(client: AsyncClient):
    response = await client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"message": "ITS ALIVE!!!"}


@pytest.mark.asyncio
async def test_db_first_element(client: AsyncClient):
    response = await client.get("/db/music-halls/1")
    assert response.status_code == 200

    hall_1 = {
        "id": 1,
        "city": "Beit 2",
        "hall_name": "Kameri 1",
        "email": "kameri@example.com",
        "stage": True,
        "pipe_height": 58,
        "stage_type": "raised",
    }
    assert response.json() == hall_1
