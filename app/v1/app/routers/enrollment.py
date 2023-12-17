# --------------------------------------------------------------------------
# Enrollment model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import database
from app.crud import enrollment as crud
from app.helper.exceptions import InternalException, ErrorCode
from app.schemas.requests import EnrollmentCreateDelete
from app.schemas.responses import EnrollmentSchema
from ._check import auth, check_user, check_user_is_self


log = getLogger(__name__)
enrollment_router = APIRouter(prefix="/enrollment")


@enrollment_router.get(
    "/info",
    response_model=List[EnrollmentSchema],
    summary="단일 과목 수강 신청 정보 조회",
    description="특정 과목에 대한 수강 신청 정보를 조회합니다.",
    dependencies=[Depends(auth)],
)
async def read_enrollment(
    course_id: Optional[int] = Query(None, description="조회할 과목의 ID"),
    user_id: Optional[int] = Query(None, description="조회할 사용자의 ID"),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db),
):
    if not (course_id or user_id):
        raise InternalException(
            "과목 ID 또는 사용자 ID를 지정해주세요.", error_code=ErrorCode.BAD_REQUEST
        )
    db_enrollment = await crud.get_enrollments(
        db, course_id, user_id, skip=skip, limit=limit
    )
    if db_enrollment is None:
        raise InternalException("해당 과목을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND)
    return db_enrollment


@enrollment_router.post(
    "",
    response_model=EnrollmentSchema,
    summary="단일 과목 수강 신청",
    description="특정 과목에 대한 수강 신청을 진행합니다.",
    dependencies=[Depends(auth)],
)
async def create_enrollment(
    enrollment: EnrollmentCreateDelete,
    db: AsyncSession = Depends(database.get_db),
    request_user=Depends(check_user),
):
    user_pk = request_user
    await check_user_is_self(db=db, user_pk=int(user_pk), target_pk=enrollment.user_id)

    return await crud.create_enrollment(db, enrollment)


@enrollment_router.post(
    "/abandon",
    status_code=204,
    summary="단일 과목 수강 포기",
    description="특정 과목에 대한 수강 포기를 진행합니다.",
    dependencies=[Depends(auth)],
)
async def delete_enrollment(
    enrollment: EnrollmentCreateDelete,
    db: AsyncSession = Depends(database.get_db),
    request_user=Depends(check_user),
):
    user_pk = request_user
    await check_user_is_self(db=db, user_pk=int(user_pk), target_pk=enrollment.user_id)

    db_enrollment = await crud.delete_enrollment(db, enrollment)
    if db_enrollment is None:
        raise InternalException("수강 신청 정보를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND)
