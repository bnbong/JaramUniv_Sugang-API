# --------------------------------------------------------------------------
# Backend Application과 router을 연결하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import APIRouter

from .user import user_router

# from .item import item_router
# from .timetable import timetable_router

router = APIRouter(prefix="/api")


@router.get("/ping")
async def ping():
    return {"ping": "pong"}


router.include_router(user_router, tags=["user"])
