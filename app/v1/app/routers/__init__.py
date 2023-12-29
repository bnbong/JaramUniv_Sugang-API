# --------------------------------------------------------------------------
# Backend Application과 router을 연결하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import APIRouter

from .user import user_router
from .course import course_router
from .enrollment import enrollment_router

router = APIRouter(prefix="/jaram-sugang/v1")


@router.get("/ping")
async def ping():
    return {"ping": "pong"}


router.include_router(user_router, tags=["user"])
router.include_router(course_router, tags=["course"])
router.include_router(enrollment_router, tags=["enrollment"])
