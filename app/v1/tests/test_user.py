# --------------------------------------------------------------------------
# User의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient


async def _create_user(
    app_client: AsyncClient,
    email: str,
    real_name: str,
    user_type: str,
    department_code: str,
):
    """Helper function to create a user and return the user's info"""
    response = await app_client.post(
        "api/user/",
        json={
            "email": email,
            "real_name": real_name,
            "user_type": user_type,
            "department_code": department_code,
        },
    )
    return response.json()


class TestUserAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        self.test_user = await _create_user(
            app_client,
            "test@testmail.com",
            "John Doe",
            "student",
            "SW100",
        )

    async def test_create_user(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.post(
            "api/user/",
            json={
                "email": "new_user@testmail.com",
                "real_name": "New User",
                "user_type": "student",
                "department_code": "AI222",
            },
        )

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["email"] == "new_user@testmail.com"
        assert data["real_name"] == "New User"
        assert data["user_type"] == "student"
        assert data["department_code"] == "AI222"

    async def test_get_user(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(f"api/user/{self.test_user['id']}")

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["email"] == "test@testmail.com"
        assert data["real_name"] == "John Doe"
        assert data["user_type"] == "student"
        assert data["department_code"] == "SW100"

    async def test_edit_user(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.put(
            f"api/user/{self.test_user['id']}",
            json={"email": "another_test@testmail.com"},
        )

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["email"] == "another_test@testmail.com"
        assert data["real_name"] == "John Doe"
        assert data["user_type"] == "student"
        assert data["department_code"] == "SW100"

        # when
        response = await app_client.put(
            f"api/user/{self.test_user['id']}",
            json={"real_name": "Jane Doe"},
        )

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["email"] == "another_test@testmail.com"
        assert data["real_name"] == "Jane Doe"
        assert data["user_type"] == "student"
        assert data["department_code"] == "SW100"

    async def test_delete_user(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.delete(f"api/user/{self.test_user['id']}")

        # then
        assert response.status_code == 204

        # when
        response = await app_client.get(f"api/user/{self.test_user['id']}")

        # then
        assert response.status_code == 404
        assert response.json() == {"detail": "해당 유저를 찾을 수 없습니다."}

    async def test_get_students(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("/api/user/students")

        # then
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 6

    async def test_get_professors(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("/api/user/instructors")

        # then
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 3
