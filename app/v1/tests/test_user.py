# --------------------------------------------------------------------------
# User의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient


class TestUserAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        pass  # TODO: 유저(학생)생성 로직 추가

    async def test_get_students(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("/api/user/students")

        # then
        data = response.json()
        assert response.status_code == 200
        print(data)
