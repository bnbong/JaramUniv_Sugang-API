# # app/context.py
# from __future__ import annotations

# import uuid
# import contextlib

# from contextvars import ContextVar
# from typing import AsyncIterator, NamedTuple, TYPE_CHECKING

# if TYPE_CHECKING:
#     from .db.connection import MariaDBConnectionFactory
#     from .settings import Settings


# current_app_context: ContextVar[AppContext] = ContextVar("current_app_context")


# class current_app_context_getter:
#     def __get__(self, obj, objtype=None):
#         current_session = current_app_context.get()
#         if current_session is None:
#             raise LookupError("bind your local thread context first.")
#         print(current_session)
#         return current_session


# class AppContext(NamedTuple):
#     if TYPE_CHECKING:
#         current: AppContext
#     settings: Settings
#     db: MariaDBConnectionFactory

#     id: str | None = None


# async def create_app_context(settings: Settings) -> AppContext:
#     from .db.connection import MariaDBConnectionFactory

#     return AppContext(
#         settings=settings,
#         db=MariaDBConnectionFactory(database_uri=settings.DB_URI)
#     )


# @contextlib.asynccontextmanager
# async def bind_app_context(app_context: AppContext) -> AsyncIterator[None]:
#     print(current_app_context)
#     context_token = current_app_context.set(app_context._replace(id=str(uuid.uuid4())))
#     try:
#         yield
#     finally:
#         try:
#             await app_context.db.clear_scoped_session()
#         except Exception:
#             print("Failed to clear scoped session.")

#         current_app_context.reset(context_token)

# AppContext.current = current_app_context_getter()

# # async def link_current_context(settings: Settings) -> AsyncIterator[None]:
# #     from .db.connection import MariaDBConnectionFactory

# #     context = AppContext(settings=settings, db=MariaDBConnectionFactory(database_uri=settings.DB_URI))._replace(id=str(uuid.uuid4()))
# #     try:
# #         yield
# #     finally:
# #         try:
# #             await context.db.clear_scoped_session()
# #         except Exception:
# #             print("Failed to clear scoped session")
