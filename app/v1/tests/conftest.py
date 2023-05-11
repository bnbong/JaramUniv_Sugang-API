import pytest
import pytest_asyncio

import uvloop

from asyncio import AbstractEventLoop
from typing import AsyncIterator, Iterator
from httpx import AsyncClient
# from asgi_lifespan import LifespanManager

from app import create_app
from app.settings import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(_env_file=".env.test")


@pytest.fixture(scope="class")
def event_loop() -> Iterator[AbstractEventLoop]:
    loop = uvloop.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="class")
async def app_client(settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(settings=settings)
    async with AsyncClient(
        app=app, base_url="http://test"
    ) as app_client:
        yield app_client
