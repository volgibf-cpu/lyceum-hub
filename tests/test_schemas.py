import pytest
from src.schemas.schemas import LoginRequest
from pydantic import ValidationError


def test_login_email_password():
    user_login = LoginRequest(email="volgibf@gmail.com", password="fer123")

    assert user_login.email == "volgibf@gmail.com"
    assert user_login.password == "fer123"

def test_login_validate():
    with pytest.raises(ValidationError):
        LoginRequest(email="dsadsa", password="12345")


