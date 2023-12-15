# --------------------------------------------------------------------------
# Enrollment model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import database
from app.crud import enrollment as crud
from app.schemas.requests import EnrollmentCreate
from app.schemas.responses import EnrollmentSchema


log = getLogger(__name__)
enrollment_router = APIRouter(prefix="/enrollment")


@enrollment_router.get(
    "/{course_id}",
    response_model=List[EnrollmentSchema],
    summary="단일 과목 수강 신청 정보 조회",
    description="특정 과목에 대한 수강 신청 정보를 조회합니다.",
)
async def read_enrollment(
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db),
):
    db_enrollment = await crud.get_enrollments(db, course_id, skip=skip, limit=limit)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="해당 과목을 찾을 수 없습니다.")
    return db_enrollment


# 단일 과목에 대하여 수강 신청 : POST. 수강 신청 인원(course_capacity)가 꽉 차있는 경우 수강 신청이 불가, 교수는 수강 신청 X

# 특정 회원의 수강신청 정보 조회 : GET

# 특정 괌고을 수강 신청한 전체 회원 정보 조회 : GET

# 단일 과목에 대하여 수강 포기 : DELETE, 교수는 수강 포기 X
