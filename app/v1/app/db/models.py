# --------------------------------------------------------------------------
# 자람 수강 앱의 model ORM을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from ._base import ModelBase


class Course(ModelBase):  # 개설 과목
    __tablename__ = "COURSE"

    id = Column(Integer, primary_key=True)
    course_name = Column(String(length=90), nullable=False)
    course_description = Column(String(length=255), nullable=False)
    course_capacity = Column(Integer, nullable=False)

    department_code = Column(String(length=5), ForeignKey("DEPARTMENT.code"), nullable=False)
    professor_id = Column(Integer, ForeignKey("USER.id"), nullable=False)

    department = relationship("Department", back_populates="courses")
    professor = relationship("User", back_populates="courses", lazy="selectin")
    enrollments = relationship("Enrollment", back_populates="course", lazy="selectin")


class Department(ModelBase):  # 학과
    __tablename__ = "DEPARTMENT"

    code = Column(String(length=5), primary_key=True)
    name = Column(String(length=255), nullable=False)

    courses = relationship("Course", back_populates="department")


class Enrollment(ModelBase):  # 수강 신청 정보
    __tablename__ = "ENROLLMENT"

    id = Column(Integer, primary_key=True)
    enrollment_time = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("USER.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("COURSE.id"), nullable=False)

    user = relationship("User", back_populates="enrollments", lazy="selectin")
    course = relationship("Course", back_populates="enrollments")


class User(ModelBase):  # 회원 정보
    __tablename__ = "USER"

    id = Column(Integer, primary_key=True)
    email = Column(String(length=256), unique=True, nullable=False)
    real_name = Column(String(length=30), nullable=False)
    user_type = Column(Enum("student", "instructor", name="user_type"), nullable=False)

    department_code = Column(String(length=5), ForeignKey("DEPARTMENT.code"), nullable=False)

    courses = relationship("Course", back_populates="professor")
    enrollments = relationship("Enrollment", back_populates="user")
