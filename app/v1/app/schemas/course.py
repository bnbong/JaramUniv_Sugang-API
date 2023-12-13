# --------------------------------------------------------------------------
# Course model의 schema를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from pydantic import BaseModel, Field

from app.db.models import Course
from app.schemas.enrollment import EnrolledUserSchema
from app.schemas.user import UserSchema


class CourseCreate(BaseModel):
    course_name: str
    course_description: str
    course_capacity: int
    department_code: str
    professor_name: str


class CourseSchema(BaseModel):
    id: int = Field(..., title="Course's ID (pk)", description="과목의 고유 식별자입니다.")
    course_name: str
    course_description: str
    course_capacity: int
    department_code: str

    professor_info: UserSchema = Field(
        validation_alias="professor"
    )

    enrolled_students: list[EnrolledUserSchema] = Field(
        validation_alias="enrollments"
    )

    class Config:
        from_attributes = True

