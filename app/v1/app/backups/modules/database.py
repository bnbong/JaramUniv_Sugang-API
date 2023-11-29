# from sqlalchemy.ext.asyncio import (
#     AsyncEngine,
#     AsyncSession,
#     async_scoped_session,
#     create_async_engine,
# )
# from sqlalchemy.orm import sessionmaker

# from app.context import AppContext


# # Create MariaDB connection session
# class MariaDBConnection:
#     def __init__(self, db_uri: str):
#         self.engine: AsyncEngine = create_async_engine(
#             db_uri,
#             connect_args={
#                 # to disable SQLA's statement cache for `.prepare()`
#                 "prepared_statement_cache_size": 0,
#                 # to disable asyncpg's statement cache for `.execute()`
#                 "statement_cache_size": 0,
#             },
#         )

#         self._scoped_session = async_scoped_session(
#             sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession),
#             scopefunc=AppContext.current.id,
#         )

#     @property
#     def session(self) -> AsyncSession:
#         return self._scoped_session()
