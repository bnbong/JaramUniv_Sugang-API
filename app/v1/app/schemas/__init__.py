# --------------------------------------------------------------------------
# 각종 schema를 정의합니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum


class UserType(str, Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"
