# --------------------------------------------------------------------------
# 자람 수강 앱의 model ORM을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from ._base import ModelBase


class Course(ModelBase):
    __tablename__ = "COURSE"

    id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)
    course_description = Column(String, nullable=False)
    course_capacity = Column(Integer, nullable=False)

    department_code = Column(Integer, ForeignKey("DEPARTMENT.code"), nullable=False)
    professor_id = Column(Integer, ForeignKey("USER.id"), nullable=False)

    department = relationship("Department", back_populates="courses")
    professor = relationship("User", back_populates="courses")


class Department(ModelBase):
    __tablename__ = "DEPARTMENT"

    code = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    courses = relationship("Course", back_populates="department")


class Enrollment(ModelBase):
    __tablename__ = "ENROLLMENT"

    id = Column(Integer, primary_key=True)
    enrollment_time = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("USER.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("COURSE.id"), nullable=False)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class User(ModelBase):
    __tablename__ = "USER"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    real_name = Column(String, nullable=False)
    user_type = Column(Enum("student", "instructor", name="user_type"), nullable=False)

    department_code = Column(Integer, ForeignKey("DEPARTMENT.code"), nullable=False)

    courses = relationship("Course", back_populates="professor")
    enrollments = relationship("Enrollment", back_populates="user")
