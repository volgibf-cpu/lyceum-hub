import pytest
from src.schemas.schemas import LoginRequest, UserResponse, GradeRequest
from pydantic import ValidationError


def test_login_email_password():
    user_login = LoginRequest(email="volgibf@gmail.com", password="fer123")

    assert user_login.email == "volgibf@gmail.com"

def test_user_response():
    user = UserResponse(id=1,
                        email="user@gmail.com",
                        first_name="Alex",
                        last_name="Sebastian",
                        middle_name="Feliach",
                        birth_date="2010-12-03",
                        role="student")

    assert user.email == "user@gmail.com"
    assert user.birth_date.year == 2010
    assert user.birth_date.month == 12
    assert user.birth_date.day == 3

def test_grade_request():
    grade = GradeRequest(student_id=1,
                         subject_name="Математика",
                         kind="absence",
                         status="Н",
                         date="2026-10-13")

    assert grade.value is None
    assert grade.comment is None
    assert grade.date.year == 2026
    assert grade.date.month == 10
    assert grade.date.day == 13

def test_login_invalid_email():
    with pytest.raises(ValidationError):
        user_login = LoginRequest(email="sumit1213FER", 
                                  password="fer421")

def test_user_invalid_birth_date():
    with pytest.raises(ValidationError):
        user = UserResponse(id=1,
                            email="user@gmail.com",
                            first_name="Alex",
                            last_name="Sebastian",
                            middle_name="Feliach",
                            birth_date="2010.12.03",
                            role="student")

