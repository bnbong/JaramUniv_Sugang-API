from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/fetch-db", include_in_schema=False)
async def fetch_maria_db() -> JSONResponse:
    pass
