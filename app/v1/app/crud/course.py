# --------------------------------------------------------------------------
# Course model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._base import get_objects, create_object, update_object
from app.db.models import User, Course, Enrollment
from app.schemas.requests import CourseCreate, CourseUpdate
from app.schemas.responses import CourseDetailSchema, UserSchema


async def get_user_by_name(db: AsyncSession, name: str) -> Optional[UserSchema]:
    query = select(User).filter(User.real_name == name)
    result = (await db.execute(query)).scalar_one_or_none()
    if result:
        return UserSchema.model_validate(result.__dict__)
    else:
        return None


async def get_courses(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[CourseDetailSchema]:
    return await get_objects(
        db=db,
        model=Course,
        response_model=CourseDetailSchema,
        skip=skip,
        limit=limit,
    )


async def get_course(db: AsyncSession, course_id: int) -> Optional[CourseDetailSchema]:
    query = select(Course).filter(Course.id == course_id)
    result = (await db.execute(query)).scalar_one_or_none()
    if result:
        return CourseDetailSchema.model_validate(result.__dict__)
    else:
        return None


async def get_enrolled_students(db: AsyncSession, course_id: int) -> List[UserSchema]:
    query = select(User).join(Enrollment).filter(Enrollment.course_id == course_id)
    result = await db.execute(query)
    result_list = result.scalars().all()
    return [UserSchema.model_validate(item.__dict__) for item in result_list]


async def create_course(db: AsyncSession, course: CourseCreate) -> CourseDetailSchema:
    return await create_object(
        db=db, model=Course, obj=course, response_model=CourseDetailSchema
    )


async def update_course(
    db: AsyncSession, course_id: int, course: CourseUpdate
) -> Optional[CourseDetailSchema]:
    return await update_object(
        db=db,
        model=Course,
        model_id=course_id,
        obj=course,
        response_model=CourseDetailSchema,
    )


async def delete_course(db: AsyncSession, course_id: int) -> Optional[int]:
    enrollments = await db.execute(
        select(Enrollment).filter(Enrollment.course_id == course_id)
    )
    for enrollment in enrollments.scalars().all():
        await db.delete(enrollment)

    db_course = await db.get(Course, course_id)
    if db_course:
        await db.delete(db_course)
        await db.commit()
        return course_id
    else:
        return None
