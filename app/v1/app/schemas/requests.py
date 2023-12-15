# --------------------------------------------------------------------------
# Request schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas import UserType


# --------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------
class UserCreate(BaseModel):
    email: str = Field(..., title="User's Email", description="유저의 이메일 주소입니다.")
    real_name: str = Field(
        ..., title="User's Real Name", description="유저의 실명입니다. 10자를 넘기지 않으며, 모두 한글입니다."
    )
    user_type: UserType = Field(
        ..., title="User's Type", description="유저의 타입입니다. 학생인지 교수인지를 나타냅니다."
    )
    department_code: str = Field(
        ..., title="User's Department Code", description="유저의 소속 학과 코드입니다."
    )


class UserUpdate(BaseModel):
    email: str = Field(
        None,
        title="User's Email",
        description="유저의 이메일 주소입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )
    real_name: str = Field(
        None,
        title="User's Real Name",
        description="유저의 실명입니다. 10자를 넘기지 않으며, 모두 한글입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )
    user_type: UserType = Field(
        None,
        title="User's Type",
        description="유저의 타입입니다. 학생인지 교수인지를 나타냅니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )
    department_code: str = Field(
        None,
        title="User's Department Code",
        description="유저의 소속 학과 코드입니다. 이 필드를 비워두면 업데이트하지 않습니다.",
    )


# --------------------------------------------------------------------------
# Course
# --------------------------------------------------------------------------
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


# --------------------------------------------------------------------------
# Enrollment
# --------------------------------------------------------------------------
class EnrollmentCreate(BaseModel):
    course_id: int = Field(
        ..., title="Enrollment's Course ID", description="수강 신청할 과목의 ID입니다."
    )
    student_id: int = Field(
        ..., title="Enrollment's Student ID", description="수강 신청할 학생의 ID입니다."
    )
