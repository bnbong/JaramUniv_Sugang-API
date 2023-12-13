# --------------------------------------------------------------------------
# User model의 schema를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum
from pydantic import BaseModel, Field


class UserType(str, Enum):
    student = "student"
    instructor = "instructor"


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
