# --------------------------------------------------------------------------
# Backend Application과 router을 연결하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import APIRouter

# from .member import member_router
# from .item import item_router
# from .timetable import timetable_router

router = APIRouter(prefix="/api/v1")

# router.include_router(member_router, tags=["member"])
