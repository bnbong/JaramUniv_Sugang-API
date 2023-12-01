# --------------------------------------------------------------------------
# User model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ._base import get_objects
from app.db.models import User
from app.schemas import user as schema


async def get_all_students(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[schema.UserSchema]:
    return await get_objects(
        db=db,
        model=User,
        response_model=schema.UserSchema,
        condition=User.user_type == "student",
        skip=skip,
        limit=limit,
    )
