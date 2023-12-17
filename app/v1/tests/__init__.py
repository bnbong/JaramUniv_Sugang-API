# --------------------------------------------------------------------------
# Jaram 수강 신청 API의 Testcase를 정의한 모듈입니다.
#
# 본 모듈에서는 API endpoint를 사용해서 인스턴스를 생성하는 로직이 아닌
# DB에 직접적으로 입출력을 하는 메서드를 정의하였습니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from datetime import datetime

from app.db.models import Course, Enrollment
from .conftest import test_engine, AsyncSession


def make_header(user_pk: int):
    return {
        "user_pk": str(user_pk),
    }


async def _create_test_course_at_db(
    course_name: str,
    course_description: str,
    course_capacity: int,
    professor_id: int,
    department_code: str,
):
    async with AsyncSession(bind=test_engine) as session:
        test_board = Course(
            course_name=course_name,
            course_description=course_description,
            course_capacity=course_capacity,
            professor_id=professor_id,
            department_code=department_code,
        )
        session.add(test_board)
        await session.commit()
        await session.refresh(test_board)


async def _create_enrollment_at_db(user_id: int, course_id: int):
    async with AsyncSession(bind=test_engine) as session:
        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            enrollment_time=datetime.now(),  # 현재 시간을 수강 신청 시간으로 설정
        )
        session.add(enrollment)
        await session.commit()
        await session.refresh(enrollment)
