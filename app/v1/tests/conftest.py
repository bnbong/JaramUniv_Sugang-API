# --------------------------------------------------------------------------
# pytest의 configuration을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import uvloop
import pytest
import pytest_asyncio

from typing import Iterator, AsyncIterator
from asyncio import AbstractEventLoop

from asgi_lifespan import LifespanManager

from httpx import AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.db.database import Base, get_db
from app.db.models import Department
from app.core.settings import AppSettings
from app import create_app
from tests.test_user import _create_user

app_settings = AppSettings(_env_file=".env.test")


test_engine = create_async_engine(
    str(app_settings.DATABASE_URI), **app_settings.DATABASE_OPTIONS
)


async def get_test_db():
    test_session_local = AsyncSession(bind=test_engine)  # type: ignore
    try:
        yield test_session_local
    finally:
        await test_session_local.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db():
    print("initialize test database")
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    loop = uvloop.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def app_client() -> AsyncIterator[AsyncClient]:
    app = create_app(app_settings)
    app.dependency_overrides[get_db] = get_test_db

    async with AsyncClient(
        app=app, base_url="http://test"
    ) as app_client, LifespanManager(app):
        yield app_client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_department_data(init_db):
    async with AsyncSession(bind=test_engine) as session:
        departments = [
            Department(code="SW100", name="소프트웨어학과"),
            Department(code="AI222", name="인공지능학과"),
            Department(code="ICT12", name="ICT 융합학과"),
            Department(code="PYS12", name="물리학과"),
            Department(code="MATH1", name="수학과"),
            Department(code="DUKNW", name="구근모를아십니과"),
            Department(code="TP100", name="내거친생각과"),
            Department(code="DLA73", name="불안한눈빛과"),
            Department(code="ABCDE", name="그걸지켜보는과"),
        ]
        session.add_all(departments)
        await session.commit()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_user_data(app_client: AsyncClient):
    for i in range(5):
        await _create_user(
            app_client,
            f"test{i}@testmail.com",
            f"Test User {i}",
            "student",
            "ICT12",
        )

    for i in range(3):
        await _create_user(
            app_client,
            f"professor{i}@testmail.com",
            f"Professor {i}",
            "instructor",
            "SW100",
        )

    await _create_user(
        app_client,
        "admin@testmail.com",
        "Admin",
        "admin",
        "SW100",
    )
