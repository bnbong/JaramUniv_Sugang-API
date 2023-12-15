# --------------------------------------------------------------------------
# Enrollment의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient
from datetime import datetime

from app.db.models import Course, Enrollment
from .conftest import test_engine, AsyncSession
from .test_course import _create_test_course_at_db, _create_enrollment_at_db


class TestEnrollmentAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        pass

    async def test_get_enrollments(self, app_client: AsyncClient):
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

        # when
        response = await app_client.get("api/enrollment/1")

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data) == 2
        assert response_data[0]["course_id"].get('id') == 1
        assert response_data[0]["student_id"].get('id') == 1
        assert response_data[1]["course_id"].get('id') == 1
        assert response_data[1]["student_id"].get('id') == 2

