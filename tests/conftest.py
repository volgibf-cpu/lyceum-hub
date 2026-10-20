import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.models import Base, User, Pair, Group, Grade
from src.core.database import engine, SessionLocal, get_db
from src.core.security import hash_password
from datetime import date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

test_engine = create_engine("sqlite:///:memory:",
                            connect_args={"check_same_thread": False},
                            poolclass=StaticPool, # Критично для памяти!
                            )

TestSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture
def db_session():
    session = TestSessionLocal()
    try:
        Base.metadata.create_all(test_engine)
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
        Base.metadata.drop_all(test_engine)

@pytest.fixture
def client(db_session):
    def get_overrides_db():
            yield db_session
    app.dependency_overrides[get_db] = get_overrides_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    

@pytest.fixture
def test_users(db_session):
    teacher = User(email="teacher_test@gmail.com", password=hash_password("12345"), first_name="TestTeacher", last_name="TestTeacher", middle_name="TestTeacher", birth_date=date(1990, 9, 11), role="teacher")
    
    db_session.add(teacher)
    db_session.commit()

    group = Group(name="TestGroup", year=1, curator_id=teacher.id)

    db_session.add(group)
    db_session.commit()

    student = User(email="test@gmail.com", password=hash_password("12345"), first_name="TestStudent", last_name="TestStudent", middle_name="TestStudent", birth_date=date(2010, 11, 3), role="student", group_id=group.id)

    db_session.add(student)
    db_session.commit()    
    
    yield {"teacher": teacher,
           "student": student,
           "group": group}
    
    db_session.delete(student)
    db_session.delete(group)
    db_session.delete(teacher)
    db_session.commit()

@pytest.fixture
def auth_student(client, test_users):
    client.post("/auth", json={
        "email": "test@gmail.com",
        "password": "12345"
    })

    yield client

@pytest.fixture
def auth_teacher(client, test_users):
    client.post("/auth", json={
        "email": "teacher_test@gmail.com",
        "password": "12345"
    })

    yield client
        
@pytest.fixture
def grade_test(db_session, test_users):
    grade = Grade(subject_name="Математика", student_id=test_users["student"].id, teacher_id=test_users["teacher"].id, grade_date=date(2026, 10, 3), kind="grade", value=4)

    db_session.add(grade)
    db_session.commit()

    yield grade

    db_session.delete(grade)
    db_session.commit()

@pytest.fixture
def test_pair(db_session, test_users):
    pair = Pair(teacher_id=test_users["teacher"].id, group_id=test_users["group"].id, subject_name="Математика", number=3, day="Понедельник", start="11:20", end="12:50")

    db_session.add(pair)
    db_session.commit()

    yield pair

    db_session.delete(pair)
    db_session.commit()


