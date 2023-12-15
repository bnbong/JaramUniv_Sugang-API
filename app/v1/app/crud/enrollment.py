# --------------------------------------------------------------------------
# Enrollment model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._base import get_objects, create_object, update_object
from app.db.models import User, Course, Enrollment
from app.schemas.requests import EnrollmentCreate
from app.schemas.responses import EnrollmentSchema


async def get_enrollments(
    db: AsyncSession, course_id: int, skip: int = 0, limit: int = 100
) -> List[EnrollmentSchema]:
    query = select(Enrollment).offset(skip).limit(limit).where(course_id == course_id)
    result = await db.execute(query)
    result_list = result.scalars().all()
    print(result_list[0].__dict__)
    return [EnrollmentSchema.model_validate(item.__dict__) for item in result_list]
