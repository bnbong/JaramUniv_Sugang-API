from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._base import get_objects
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
