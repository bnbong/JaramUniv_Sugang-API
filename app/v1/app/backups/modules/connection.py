# # app/db/connection
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import (
#     AsyncEngine, AsyncSession, create_async_engine, async_scoped_session
# )

# from app.context import AppContext


# class MariaDBConnectionFactory:
#     def __init__(self, database_uri: str) -> None:
#         self.engine: AsyncEngine = create_async_engine(
#             url=database_uri,
#             echo=True,  # SQL 쿼리 출력 활성화 (디버깅 목적)
#             pool_pre_ping=True,  # MariaDB에 대한 연결 상태 확인
#             pool_size=5,  # 연결 풀의 크기 설정
#             max_overflow=10,  # 연결 풀이 가득 찼을 때 새로운 연결을 허용하는 최대 개수 설정
#             connect_args={
#                 "prepared_statement_cache_size": 0,  # statement cache 비활성화
#                 "statement_cache_size": 0,
#             }
#         )

#         self._scoped_session = async_scoped_session(
#             session_factory=sessionmaker(
#                 bind=self.engine,
#                 class_=AsyncSession,
#                 autocommit=False,
#                 autoflush=False,
#                 expire_on_commit=False,
#             ),
#             scopefunc=lambda: AppContext.current.id
#         )

#     @property
#     def session(self) -> AsyncSession:
#         return self._scoped_session

#     async def clear_scoped_session(self) -> None:
#         await self._scoped_session.remove()
