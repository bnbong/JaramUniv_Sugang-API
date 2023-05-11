# # app/routers/fetch_db.py
# from fastapi import APIRouter
# from fastapi.responses import JSONResponse
# from sqlalchemy.sql import text

# from app.context import AppContext

# router = APIRouter()


# @router.get("/fetch-db", include_in_schema=False)
# async def fetch_maria_db() -> JSONResponse:
#     # try:
#     #     if (await AppContext.current.db.session.execute(text("SELECT 1"))).scalar() != 1:
#     #         raise RuntimeError("MariaDB connection failure")
#     # except Exception:
#     #     raise RuntimeError("Unknown error happens")
#     if (await AppContext.current.db.session.execute(text("SELECT 1"))).scalar() != 1:
#         raise RuntimeError("MariaDB connection failure")

#     return JSONResponse({"detail": "success"}, status_code=200)
