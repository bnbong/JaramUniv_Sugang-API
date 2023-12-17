# --------------------------------------------------------------------------
# Department model의 API router을 정의한 모듈입니다.
#
# 단, Department 정보를 수정하는 기능은 관리자 계정만 사용 가능합니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# from app.crud import course as crud
from app.db import database
from ._check import auth, check_user, check_user_is_admin

# from app.schemas import course as schemas


log = getLogger(__name__)
department_router = APIRouter(prefix="/department")


@department_router.put(
    "/",
    # response_model=List[schemas.Item],
    summary="전공 정보 수정",
    description="학과의 명칭을 변경합니다.",
    dependencies=[Depends(auth)],
)
async def update_department(
    department,
    db: AsyncSession = Depends(database.get_db),
    request_user=Depends(check_user),
):
    user_pk = request_user
    await check_user_is_admin(db, user_pk)

    pass


@department_router.post(
    "/",
    # response_model=List[schemas.Item],
    summary="전공 정보 생성",
    description="새로운 학과를 생성합니다.",
    dependencies=[Depends(auth)],
)
async def create_department(
    department,
    db: AsyncSession = Depends(database.get_db),
    request_user=Depends(check_user),
):
    user_pk = request_user
    await check_user_is_admin(db, user_pk)

    pass
