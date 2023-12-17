# --------------------------------------------------------------------------
# 헤더 관련 로직을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger

from fastapi import Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.helper.exceptions import InternalException, ErrorCode
from app.db.models import User

log = getLogger(__name__)


def auth(request: Request):
    header = request.headers
    uid = header.get("user_pk") if header.get("user_pk") else None

    if uid is None:
        raise InternalException("인증 정보가 없습니다.", ErrorCode.BAD_REQUEST)


async def check_user(
    user_pk: str = Header(
        None, description="사용자의 고유 식별자입니다.", convert_underscores=False
    ),
) -> str:
    if not user_pk:
        raise InternalException("사용자 정보가 없습니다.", ErrorCode.BAD_REQUEST)

    return user_pk


async def check_user_auth(
    db: AsyncSession,
    user_pk: str = Header(
        None, description="사용자의 고유 식별자입니다.", convert_underscores=False
    ),
):
    request_user = await db.get(User, user_pk)

    if request_user.user_type == "student":
        raise InternalException("해당 유저의 권한으로는 불가능한 작업입니다.", ErrorCode.FORBIDDEN)


async def check_user_is_admin(
    db: AsyncSession,
    user_pk: str,
):
    request_user = await db.get(User, user_pk)

    if request_user.user_type != "admin":
        raise InternalException("해당 유저의 권한으로는 불가능한 작업입니다.", ErrorCode.FORBIDDEN)


async def check_user_is_self(
    db: AsyncSession,
    user_pk: int,
    target_pk: int,
):
    request_user = await db.get(User, user_pk)

    if request_user.user_type != "admin" and user_pk != target_pk:
        raise InternalException("해당 작업은 본인만 가능합니다.", ErrorCode.FORBIDDEN)
