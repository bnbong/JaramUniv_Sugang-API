# --------------------------------------------------------------------------
# Course의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient

from tests import _create_enrollment_at_db, _create_test_course_at_db


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
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data) == 3
        assert response_data[0]["course_name"] == "test_course_0"
        assert response_data[0]["course_description"] == "test_course_description_0"
        assert response_data[0]["course_capacity"] == 30
        assert response_data[0]["department_code"] == "SW100"
        assert len(response_data[0]["enrolled_students"]) == 3
        assert response_data[0]["professor_info"]["id"] == 6

    async def test_get_course(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            "test_course",
            "test_course_description",
            30,
            6,
            "SW100",
        )

        await _create_enrollment_at_db(1, 1)
        await _create_enrollment_at_db(2, 1)
        await _create_enrollment_at_db(3, 1)

        # when
        response = await app_client.get("api/course/1")

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["course_name"] == "test_course"
        assert response_data["course_description"] == "test_course_description"
        assert response_data["course_capacity"] == 30
        assert response_data["department_code"] == "SW100"
        assert len(response_data["enrolled_students"]) == 3
        assert response_data["professor_info"]["id"] == 6

    async def test_create_course(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.post(
            "api/course/",
            json={
                "course_name": "test_course",
                "course_description": "test_course_description",
                "course_capacity": 30,
                "department_code": "SW100",
                "professor_id": 6,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["course_name"] == "test_course"
        assert response_data["course_description"] == "test_course_description"
        assert response_data["course_capacity"] == 30
        assert response_data["department_code"] == "SW100"
        assert response_data["professor_info"]["id"] == 6

    async def test_update_course(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            "test_course",
            "test_course_description",
            30,
            6,
            "SW100",
        )

        await _create_enrollment_at_db(1, 1)
        await _create_enrollment_at_db(2, 1)

        # when
        response = await app_client.put(
            "api/course/1",
            json={
                "course_description": "another_course_description",
                "course_capacity": 45,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["course_name"] == "test_course"
        assert response_data["course_description"] == "another_course_description"
        assert response_data["course_capacity"] == 45
        assert response_data["department_code"] == "SW100"
        assert len(response_data["enrolled_students"]) == 2
        assert response_data["professor_info"]["id"] == 6

    async def test_delete_course(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            "test_course",
            "test_course_description",
            30,
            6,
            "SW100",
        )

        await _create_enrollment_at_db(1, 1)

        # when
        response = await app_client.delete("api/course/1")

        # then
        assert response.status_code == 204

        # (check) when
        response_check = await app_client.get(
            "api/enrollment/info?user_id=1",
        )
        response_check_2 = await app_client.get("api/enrollment/info?course_id=1")

        # (check) then
        assert len(response_check.json()) == 0
        assert len(response_check_2.json()) == 0
