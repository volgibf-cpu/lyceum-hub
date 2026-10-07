from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date

class UserRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    role: str


class PairResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    teacher_id: int
    subject_name: str
    number: int
    day: str
    start: str
    end: str

class GradeRequest(BaseModel):
    student_id: int
    subject_name: str
    kind: str
    value: int | None = None
    status: str | None = None
    date: date
    comment: str | None = None