# --------------------------------------------------------------------------
# Course의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient
from datetime import datetime

from app.db.models import Course, Enrollment
from .conftest import test_engine, AsyncSession


async def _create_test_course_at_db(
    course_name: str,
    course_description: str,
    course_capacity: int,
    professor_id: int,
    department_code: str,
):
    async with AsyncSession(bind=test_engine) as session:
        test_board = Course(
            course_name=course_name,
            course_description=course_description,
            course_capacity=course_capacity,
            professor_id=professor_id,
            department_code=department_code,
        )
        session.add(test_board)
        await session.commit()
        await session.refresh(test_board)


async def _create_enrollment_at_db(user_id: int, course_id: int):
    async with AsyncSession(bind=test_engine) as session:
        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            enrollment_time=datetime.now()  # 현재 시간을 등록 시간으로 설정
        )
        session.add(enrollment)
        await session.commit()
        await session.refresh(enrollment)


class TestCourseAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        pass

    async def test_get_courses(self, app_client: AsyncClient):
        # given
        for i in range(3):
            await _create_test_course_at_db(
                f"test_course_{i}",
                f"test_course_description_{i}",
                30,
                6,
                "SW100",
            )

        await _create_enrollment_at_db(1, 1)
        await _create_enrollment_at_db(2, 1)
        await _create_enrollment_at_db(3, 1)

        # when
        response = await app_client.get("api/course/list")

        # then
        print(response.json())

    async def test_create_course(self, app_client: AsyncClient):
        pass

    async def test_get_course(self, app_client: AsyncClient):
        pass

    async def test_update_course(self, app_client: AsyncClient):
        pass

    async def test_delete_course(self, app_client: AsyncClient):
        pass
