# --------------------------------------------------------------------------
# Course model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._base import get_objects, create_object, update_object, delete_object
from app.db.models import User, Course
from app.schemas import user as user_schema
from app.schemas import course as schema


async def get_user_by_name(db: AsyncSession, name: str) -> Optional[schema.UserSchema]:
    query = select(User).filter(User.real_name == name)
    result = (await db.execute(query)).scalar_one_or_none()
    if result:
        return user_schema.UserSchema.model_validate(result.__dict__)
    else:
        return None


async def get_courses(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[schema.CourseSchema]:
    return await get_objects(
        db=db,
        model=Course,
        response_model=schema.CourseSchema,
        skip=skip,
        limit=limit,
    )


async def get_course(db: AsyncSession, course_id: int) -> Optional[schema.CourseSchema]:
    query = select(Course).filter(Course.id == course_id)
    result = (await db.execute(query)).scalar_one_or_none()
    if result:
        return schema.CourseSchema.model_validate(result.__dict__)
    else:
        return None


async def create_course(
    db: AsyncSession, course: schema.CourseCreate
) -> schema.CourseSchema:
    return await create_object(
        db=db, model=Course, obj=course, response_model=schema.CourseSchema
    )


async def update_course(
    db: AsyncSession, course_id: int, course: schema.CourseUpdate
) -> Optional[schema.CourseSchema]:
    return await update_object(
        db=db,
        model=Course,
        model_id=course_id,
        obj=course,
        response_model=schema.CourseSchema,
    )


async def delete_course(db: AsyncSession, course_id: int) -> Optional[int]:
    return await delete_object(db=db, model=Course, model_id=course_id)
