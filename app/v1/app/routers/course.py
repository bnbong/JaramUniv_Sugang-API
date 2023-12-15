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

from app.schemas.requests import CourseCreate, CourseUpdate
from app.schemas.responses import CourseDetailSchema


log = getLogger(__name__)
course_router = APIRouter(prefix="/course")


@course_router.get(
    "/list",
    response_model=List[CourseDetailSchema],
    summary="전체 과목 조회",
    description="모든 과목에 대한 정보를 조회합니다.",
)
async def read_courses(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading items with skip: {skip} and limit: {limit}")
    return await crud.get_courses(db, skip=skip, limit=limit)


@course_router.get(
    "/{course_id}",
    response_model=CourseDetailSchema,
    summary="단일 과목 조회",
    description="특정 과목에 대한 정보를 조회합니다.",
)
async def read_course(course_id: int, db: AsyncSession = Depends(database.get_db)):
    db_course = await crud.get_course(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="해당 과목을 찾을 수 없습니다.")
    return db_course


@course_router.post(
    "/",
    response_model=CourseDetailSchema,
    summary="과목 생성",
    description="새로운 과목을 생성합니다.",
)
async def create_course(
    course: CourseCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_course(db, course)


@course_router.put(
    "/{course_id}",
    response_model=CourseDetailSchema,
    summary="과목 수정",
    description="기존 과목의 정보를 수정합니다.",
)
async def update_course(
    course_id: int,
    course: CourseUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    db_course = await crud.get_course(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="해당 과목을 찾을 수 없습니다.")
    return await crud.update_course(db, course_id, course)


@course_router.delete(
    "/{course_id}",
    status_code=204,
    summary="과목 삭제",
    description="기존 과목을 삭제합니다.",
)
async def delete_course(course_id: int, db: AsyncSession = Depends(database.get_db)):
    db_course = await crud.get_course(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="해당 과목을 찾을 수 없습니다.")
    return await crud.delete_course(db, course_id)
