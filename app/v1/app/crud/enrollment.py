# --------------------------------------------------------------------------
# Enrollment model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Optional, List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._base import get_objects, create_object, update_object
from app.db.models import User, Course, Enrollment
from app.helper.exceptions import InternalException, ErrorCode
from app.schemas.requests import EnrollmentCreateDelete
from app.schemas.responses import EnrollmentSchema


async def get_enrollments(
    db: AsyncSession,
    course_id: Optional[int],
    user_id: Optional[int],
    skip: int = 0,
    limit: int = 100,
) -> List[EnrollmentSchema]:
    query = select(Enrollment)

    conditions = []
    if course_id:
        conditions.append(Enrollment.course_id == course_id)
    if user_id:
        conditions.append(Enrollment.user_id == user_id)

    if conditions:
        query = query.where(and_(*conditions))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return [
        EnrollmentSchema.model_validate(enrollment)
        for enrollment in result.scalars().all()
    ]


async def create_enrollment(
    db: AsyncSession, enrollment: EnrollmentCreateDelete
) -> EnrollmentSchema:
    user = await db.get(User, enrollment.user_id)
    course = await db.get(Course, enrollment.course_id)
    if not user.user_type == "student":
        raise InternalException("교수는 수강 신청이 불가능합니다.", ErrorCode.FORBIDDEN)
    if course.course_capacity <= len(course.enrollments):
        raise InternalException("수강 신청 인원이 꽉 찼습니다.", ErrorCode.FORBIDDEN)

    return await create_object(
        db=db, model=Enrollment, obj=enrollment, response_model=EnrollmentSchema
    )


async def delete_enrollment(
    db: AsyncSession, enrollment: EnrollmentCreateDelete
) -> Optional[int]:
    user = await db.get(User, enrollment.user_id)
    if not user.user_type == "student":
        raise InternalException("교수는 수강 포기가 불가능합니다.", ErrorCode.FORBIDDEN)

    enrollment_record = await db.execute(
        select(Enrollment).where(
            and_(
                Enrollment.user_id == enrollment.user_id,
                Enrollment.course_id == enrollment.course_id,
            )
        )
    )
    enrollment_record = enrollment_record.scalar_one_or_none()

    if enrollment_record:
        await db.delete(enrollment_record)
        await db.commit()

        return enrollment_record.id

    else:
        return None
