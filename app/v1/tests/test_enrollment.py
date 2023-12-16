# --------------------------------------------------------------------------
# Enrollment의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient

from tests import _create_enrollment_at_db, _create_test_course_at_db


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
        await _create_enrollment_at_db(1, 2)

        # when
        response = await app_client.get("api/enrollment/info?course_id=1")

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data) == 2
        assert response_data[0]["course_id"].get("id") == 1
        assert response_data[0]["student_id"].get("id") == 1
        assert response_data[1]["course_id"].get("id") == 1
        assert response_data[1]["student_id"].get("id") == 2

        # when
        response = await app_client.get("api/enrollment/info?user_id=1")

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data) == 2
        assert response_data[0]["course_id"].get("id") == 1
        assert response_data[0]["student_id"].get("id") == 1
        assert response_data[1]["course_id"].get("id") == 2
        assert response_data[1]["student_id"].get("id") == 1

        # when
        response = await app_client.get("api/enrollment/info?user_id=1&course_id=1")

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data) == 1
        assert response_data[0]["course_id"].get("id") == 1
        assert response_data[0]["student_id"].get("id") == 1

    async def test_create_enrollments(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            30,
            6,
            "SW100",
        )

        # when
        response = await app_client.post(
            "api/enrollment",
            json={
                "course_id": 1,
                "user_id": 3,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["course_id"].get("id") == 1
        assert response_data["student_id"].get("id") == 3

    async def test_enrolled_students(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            30,
            6,
            "SW100",
        )
        await _create_enrollment_at_db(1, 1)
        await _create_enrollment_at_db(2, 1)
        await _create_enrollment_at_db(3, 1)

        # when
        response = await app_client.get("api/course/1/students")

        # then
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data) == 3
        assert response_data[0].get("id") == 1
        assert response_data[1].get("id") == 2
        assert response_data[2].get("id") == 3

    async def test_delete_enrollments(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            30,
            6,
            "SW100",
        )
        await _create_enrollment_at_db(1, 1)
        await _create_enrollment_at_db(2, 1)
        await _create_enrollment_at_db(3, 1)

        # when
        response = await app_client.post(
            "api/enrollment/abandon",
            json={
                "course_id": 1,
                "user_id": 1,
            },
        )

        # then
        assert response.status_code == 204

        # (check) when
        response_check_1 = await app_client.get(
            "api/enrollment/info?course_id=1",
        )
        response_check_2 = await app_client.get(
            "api/enrollment/info?user_id=1",
        )
        response_check_3 = await app_client.get("api/course/1")

        # (check) then
        response_data = response_check_3.json()
        assert (len(response_check_1.json())) == 2
        assert (len(response_check_2.json())) == 0
        assert (len(response_data["enrolled_students"])) == 2


class TestEnrollmentAPIFail:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        pass

    async def test_create_enrollments_fail_not_student(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            30,
            6,
            "SW100",
        )

        # when
        response = await app_client.post(
            "api/enrollment",
            json={
                "course_id": 1,
                "user_id": 6,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 403
        assert response_data["message"] == "교수는 수강 신청이 불가능합니다."

    async def test_create_enrollments_fail_max_capacity(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            2,
            6,
            "SW100",
        )
        await _create_enrollment_at_db(1, 1)
        await _create_enrollment_at_db(2, 1)

        # when
        response = await app_client.post(
            "api/enrollment",
            json={
                "course_id": 1,
                "user_id": 3,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 403
        assert response_data["message"] == "수강 신청 인원이 꽉 찼습니다."

    async def test_create_enrollments_fail_cannot_register_twice(
        self, app_client: AsyncClient
    ):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            30,
            6,
            "SW100",
        )
        await _create_enrollment_at_db(1, 1)

        # when
        response = await app_client.post(
            "api/enrollment",
            json={
                "course_id": 1,
                "user_id": 1,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 400
        assert response_data["message"] == "데이터베이스에 중복된 값이 존재합니다."

    async def test_delete_enrollments_fail_not_student(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            30,
            6,
            "SW100",
        )

        # when
        response = await app_client.post(
            "api/enrollment/abandon",
            json={
                "course_id": 1,
                "user_id": 6,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 403
        assert response_data["message"] == "교수는 수강 포기가 불가능합니다."

    async def test_delete_enrollments_fail_not_enrolled(self, app_client: AsyncClient):
        # given
        await _create_test_course_at_db(
            f"test_course",
            f"test_course_description",
            30,
            6,
            "SW100",
        )

        # when
        response = await app_client.post(
            "api/enrollment/abandon",
            json={
                "course_id": 1,
                "user_id": 1,
            },
        )

        # then
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["message"] == "수강 신청 정보를 찾을 수 없습니다."
