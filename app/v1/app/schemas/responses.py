# --------------------------------------------------------------------------
# Response schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas import UserType


# --------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------
class UserSchema(BaseModel):
    id: int = Field(..., title="User's ID (pk)", description="유저의 고유 식별자입니다.")
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

    class Config:
        from_attributes = True


# --------------------------------------------------------------------------
# Course
# --------------------------------------------------------------------------
class EnrolledUserSchema(BaseModel):
    student: UserSchema = Field(
        None,
        title="수강 학생 정보",
        description="해당 과목을 수강한 학생들의 정보입니다.",
        validation_alias="user",
    )

    class Config:
        from_attributes = True


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

    professor_id: UserSchema = Field(
        ...,
        title="Course's Professor ID",
        description="과목의 담당 교수 ID입니다.",
        validation_alias="professor",
    )

    class Config:
        from_attributes = True


class CourseDetailSchema(BaseModel):
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


# --------------------------------------------------------------------------
# Enrollment
# --------------------------------------------------------------------------
class EnrollmentSchema(BaseModel):
    id: int = Field(
        ..., title="Enrollment's ID (pk)", description="수강 신청 정보의 고유 식별자입니다."
    )
    enrollment_time: datetime = Field(
        ..., title="Enrollment's Time", description="수강 신청한 시간입니다."
    )

    course_id: CourseSchema = Field(
        ...,
        title="Enrollment's Course ID",
        description="수강 신청한 과목의 ID입니다.",
        validation_alias="course",
    )
    student_id: UserSchema = Field(
        ...,
        title="Enrollment's Student ID",
        description="수강 신청한 학생의 ID입니다.",
        validation_alias="user",
    )

    class Config:
        from_attributes = True
