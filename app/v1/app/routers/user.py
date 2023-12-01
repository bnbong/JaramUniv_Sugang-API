# --------------------------------------------------------------------------
# User model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as crud
from app.db import database
from app.schemas import user as schemas


log = getLogger(__name__)
user_router = APIRouter(prefix="/user")


@user_router.get(
    "/students",
    response_model=List[schemas.UserSchema],
    summary="학생 회원 전체를 불러오기",
    description="모든 학생 회원에 대한 정보를 조회합니다.",
)
async def get_all_students(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading students info with skip: {skip} and limit: {limit}")
    return await crud.get_all_students(db, skip=skip, limit=limit)


@user_router.get(
    "/instructors",
    response_model=List[schemas.UserSchema],
    summary="교수 회원 전체를 불러오기",
    description="모든 교수 회원에 대한 정보를 조회합니다.",
)
async def get_all_instructors(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading instructors info with skip: {skip} and limit: {limit}")
    # return await crud.get_items(db, skip=skip, limit=limit)
    pass
