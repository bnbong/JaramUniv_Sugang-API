# # --------------------------------------------------------------------------
# # LoggingMiddleware
# #
# # 해당 LoggingMiddleware는 HTTP Response를 요청 ip, status code 등과 함께 로깅합니다.
# # 로그가 제대로 적용이 안되는 현상이 발견되어 일단은 backups 폴더에 백업해두었습니다.
# # --------------------------------------------------------------------------
# import json
# import time
# import logging
#
# from typing import Callable, Tuple
# from uuid import uuid4
#
# from starlette.types import Message
# from starlette.requests import Request
# from starlette.responses import Response
# from starlette.middleware.base import BaseHTTPMiddleware
#
# from fastapi import FastAPI
#
#
# async def set_body(request: Request):
#     """Avails the response body to be logged within a middleware as,
#     it is generally not a standard practice.
#
#        Arguments:
#        - request: Request
#        Returns:
#        - receive_: Receive
#     """
#     receive_ = await request.receive()
#
#     async def receive() -> Message:
#         return receive_
#
#     request._receive = receive
#
#
# async def _log_request(request: Request) -> dict:
#     """Logs request part
#      Arguments:
#     - request: Request
#
#     """
#
#     path = request.url.path
#     if request.query_params:
#         path += f"?{request.query_params}"
#
#     request_logging = {
#         "method": request.method,
#         "path": path,
#         "ip": request.client.host,
#     }
#
#     try:
#         body = await request.json()
#         request_logging["body"] = body
#     except:
#         body = None
#
#     return request_logging
#
#
# class AsyncIteratorWrapper:
#     """The following is a utility class that transforms a
#     regular iterable to an asynchronous one.
#
#     link: https://www.python.org/dev/peps/pep-0492/#example-2
#     """
#
#     def __init__(self, obj):
#         self._it = iter(obj)
#
#     def __aiter__(self):
#         return self
#
#     async def __anext__(self):
#         try:
#             value = next(self._it)
#         except StopIteration:
#             raise StopAsyncIteration
#         return value
#
#
# class RouterLoggingMiddleware(BaseHTTPMiddleware):
#     """로그를 기록하는 로그 미들웨어의 핵심 클래스입니다.
#
#     Internal Server Error가 아닌 요청의 경우 다음과 같은 형식의 로그가 기록됩니다.
#     {
#         "X-API-REQUEST-ID": "uuid",  # X-API-REQUEST-ID maps each request-response to a unique ID
#         "request": {
#             "method": "HTTP 메서드",
#             "path": "요청 경로",
#             "ip": "요청을 보낸 유저의 ip",
#             "body": "(GET 요청의 경우 생략) 요청 body"
#         },
#         "response": {
#             "status": "successful (status code 200, 300 번대) / fail (status code 400번대)",
#             "status_code": HTTP status code,
#             "time_taken": "요청-응답 시간",
#             "body": {
#                 "response body 내용. status code 400 번대 오류의 경우, 에러 메시지"
#             }
#     """
#
#     def __init__(self, app: FastAPI, *, logger: str) -> None:
#         logger = logging.getLogger(logger)
#
#         self._logger = logger
#         super().__init__(app)
#
#     async def dispatch(self, request: Request, call_next: Callable) -> Response:
#         request_id: str = str(uuid4())
#         logging_dict = {
#             "X-API-REQUEST-ID": request_id  # X-API-REQUEST-ID maps each request-response to a unique ID
#         }
#
#         await set_body(request)
#
#         response, response_dict = await self._log_response(
#             call_next, request, request_id
#         )
#         request_dict = await _log_request(request)
#         logging_dict["request"] = request_dict
#         logging_dict["response"] = response_dict
#
#         self._logger.info(logging_dict)
#
#         return response
#
#     async def _log_response(
#         self, call_next: Callable, request: Request, request_id: str
#     ) -> Tuple[Response, dict]:
#         """Logs response part
#
#         Arguments:
#         - call_next: Callable (To execute the actual path function and get response back)
#         - request: Request
#         - request_id: str (uuid)
#         Returns:
#         - response: Response
#         - response_logging: dict
#         """
#
#         start_time = time.perf_counter()
#         response = await self._execute_request(call_next, request, request_id)
#         finish_time = time.perf_counter()
#
#         overall_status = (
#             "successful"
#             if response is not None and response.status_code < 400
#             else "failed"
#         )
#         execution_time = finish_time - start_time
#
#         response_logging = {
#             "status": overall_status,
#             "status_code": response.status_code,
#             "time_taken": f"{execution_time:0.4f}s",
#         }
#
#         resp_body = [section async for section in response.__dict__["body_iterator"]]
#         response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))
#
#         try:
#             resp_body = json.loads(resp_body[0].decode())
#         except:
#             resp_body = str(resp_body)
#
#         response_logging["body"] = resp_body
#
#         return response, response_logging
#
#     async def _execute_request(
#         self, call_next: Callable, request: Request, request_id: str
#     ) -> Response:
#         """Executes the actual path function using call_next.
#         It also injects "X-API-Request-ID" header to the response.
#
#         Arguments:
#         - call_next: Callable (To execute the actual path function
#                      and get response back)
#         - request: Request
#         - request_id: str (uuid)
#         Returns:
#         - response: Response
#         """
#         try:
#             response: Response = await call_next(request)
#
#             # Kickback X-Request-ID
#             response.headers["X-API-Request-ID"] = request_id
#             return response
#
#         except Exception as e:
#             self._logger.exception(
#                 {"path": request.url.path, "method": request.method, "reason": e}
#             )
#
