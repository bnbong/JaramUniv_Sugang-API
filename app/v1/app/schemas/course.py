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
    course_name: str = Field(..., title="Course's Name", description="생성할 과목의 이름입니다.")
    course_description: str = Field(
        ..., title="Course's Description", description="생성할 과목의 설명입니다."
    )
    course_capacity: int = Field(
        ..., title="Course's Capacity", description="생성할 과목의 수용 인원입니다."
    )
    department_code: str = Field(
        ..., title="Course's Department Code", description="생성할 과목의 소속 학과 코드입니다."
    )
    professor_id: int = Field(
        ..., title="Course's Professor ID", description="생성할 과목의 담당 교수 ID입니다."
    )


class CourseUpdate(BaseModel):
    course_name: str = Field(
        None,
        title="Course's Name",
        description="과목의 이름입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )
    course_description: str = Field(
        None,
        title="Course's Description",
        description="과목의 설명입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )
    course_capacity: int = Field(
        None,
        title="Course's Capacity",
        description="과목의 수용 인원입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )
    department_code: str = Field(
        None,
        title="Course's Department Code",
        description="과목의 소속 학과 코드입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )
    professor_id: int = Field(
        None,
        title="Course's Professor ID",
        description="과목의 담당 교수 ID입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )


class CourseSchema(BaseModel):
    id: int = Field(..., title="Course's ID (pk)", description="과목의 고유 식별자입니다.")
    course_name: str = Field(..., title="Course's Name", description="과목의 이름입니다.")
    course_description: str = Field(
        ..., title="Course's Description", description="과목의 설명입니다."
    )
    course_capacity: int = Field(
        ..., title="Course's Capacity", description="과목의 수용 인원입니다."
    )
    department_code: str = Field(
        ..., title="Course's Department Code", description="과목의 소속 학과 코드입니다."
    )

    professor_info: UserSchema = Field(
        ...,
        title="Course's Professor Info",
        description="과목의 담당 교수 정보입니다.",
        validation_alias="professor",
    )

    enrolled_students: list[EnrolledUserSchema] = Field(
        ...,
        title="Course's Enrolled Students",
        description="과목에 등록된 학생들의 정보입니다.",
        validation_alias="enrollments",
    )

    class Config:
        from_attributes = True
