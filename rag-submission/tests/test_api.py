import pytest
import pytest_asyncio

from httpx import (
    AsyncClient,
    ASGITransport,
)

from app.main import app

from app.db.database import (
    engine,
    Base,
)


@pytest_asyncio.fixture(autouse=True)
async def setup_db():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.drop_all
        )

        await conn.run_sync(
            Base.metadata.create_all
        )

    yield


@pytest_asyncio.fixture
async def client():

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:

        yield ac


@pytest.mark.asyncio
async def test_health(client):

    response = await client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_invalid(client):

    response = await client.post(
        "/api/v1/documents/upload",
        files={
            "file": (
                "test.xyz",
                b"data",
                "application/octet-stream",
            )
        },
    )

    assert response.status_code == 400