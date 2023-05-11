import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_app(app_client: AsyncClient) -> None:
    # async with with_app_context(settings):
    #     await make_fresh_db()
    response = await app_client.get("/fetch-db")

    print(response.json())

    # assert response.status_code == 200
    # assert response.json() == {"detail": "success"}
