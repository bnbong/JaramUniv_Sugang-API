# import functools

from fastapi import FastAPI
# from fastapi import Request, Response
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .settings import Settings
# from .context import create_app_context, bind_app_context, AppContext
from .routers import ALL_ROUTERS


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI()

    # app.add_event_handler(
    #     "startup", functools.partial(app_startup, app, settings)
    # )

    # app.add_event_handler(
    #     "shutdown", functools.partial(app_shutdown, app)
    # )

    for api_router in ALL_ROUTERS:
        app.include_router(api_router)

    return app


# async def app_startup(app: FastAPI, settings: Settings) -> None:
#     app_context = await create_app_context(settings=settings)

#     app.extra["_app_context"] = app_context

#     async def _ctx_middleware(
#         request: Request, call_next: RequestResponseEndpoint
#     ) -> Response:
#         async with bind_app_context(app_context=app_context):
#             response = await call_next(request)
#         return response

#     app.add_middleware(BaseHTTPMiddleware, dispatch=_ctx_middleware)


# async def app_shutdown(app: FastAPI) -> None:
#     app_context: AppContext = app.extra["_app_context"]

#     try:
#         await app_context.db.engine.dispose()
#     except Exception:
#         print("Failed to dispose DB engine.")
