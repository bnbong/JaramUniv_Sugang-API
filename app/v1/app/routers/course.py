# --------------------------------------------------------------------------
# Course model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import course as crud
from app.db import database

from app.schemas import course as schemas


log = getLogger(__name__)
course_router = APIRouter(prefix="/course")


@course_router.get(
    "/list",
    response_model=List[schemas.CourseSchema],
    summary="Read items",
    description="Read items",
)
async def read_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading items with skip: {skip} and limit: {limit}")
    return await crud.get_courses(db, skip=skip, limit=limit)
