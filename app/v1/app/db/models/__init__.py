from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import object_session
from sqlalchemy.ext.declarative import declarative_base

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @property
    def object_session(self) -> Session:
        return object_session(self)
