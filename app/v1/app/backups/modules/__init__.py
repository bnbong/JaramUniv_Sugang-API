# # tests/__init__.py

# import contextlib

# from typing import AsyncIterator

# from app.context import AppContext, bind_app_context, create_app_context
# from app.settings import Settings
# from app.db.models import BaseModel


# @contextlib.asynccontextmanager
# async def with_app_context(settings: Settings) -> AsyncIterator:
#     app_context = await create_app_context(settings=settings)
#     async with bind_app_context(app_context=app_context):
#         yield app_context


# async def make_fresh_db() -> None:
#     async with AppContext.current.db.engine.begin() as conn:
#         await conn.run_sync(BaseModel.metadata.drop_all)
#         await conn.run_sync(BaseModel.metadata.create_all)
