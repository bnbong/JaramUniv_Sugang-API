from .fetch_db import router as fetch_db_router

__all__ = ["ALL_ROUTERS"]

ALL_ROUTERS = [
    fetch_db_router
]