# --------------------------------------------------------------------------
# Course model의 schema를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from pydantic import BaseModel, Field

# from app.db.models import Course
from app.schemas.user import UserSchema


class EnrolledUserSchema(BaseModel):
    student: UserSchema = Field(
        validation_alias="user"
    )

    class Config:
        from_attributes = True
