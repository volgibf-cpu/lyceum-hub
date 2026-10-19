import pytest
from datetime import date

def test_set_grade(test_users, client):

    login_response = client.post("/auth", json={
        "email": "teacher_test@gmail.com",
        "password": "12345"
    })
    
    response = client.post("/grade/set", json={
        "student_id": test_users["student"].id,
        "subject_name": "Математика",
        "kind": "grade",
        "value": 4,
        "status": None,
        "date": "2026-10-19",
        "comment": None
    })


    assert login_response.status_code == 200
    assert response.status_code == 200
    assert response.json()["message"] == "Оценка успешно выставлена!"


def test_get_students_grades(grade_test, test_users, client):
    
    login_response = client.post("/auth", json={
            "email": "teacher_test@gmail.com",
            "password": "12345"
        })
    assert login_response.status_code == 200


    response = client.get("/grade/group")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1

    assert any(str(g["student_id"]) == str(test_users["student"].id) for g in data)
    

def test_student_grades(test_users, client, grade_test):
    
    login_response = client.post("/auth", json={
                "email": "teacher_test@gmail.com",
                "password": "12345"
            })
    assert login_response.status_code == 200

    response = client.get("/grade/student", params={"user_id": test_users["student"].id})
    assert response.status_code == 200

    data = response.json()

    grade = data[0]
    assert grade["student"] != "—"
    assert grade["teacher"] != "—"

    

def test_my_grades(test_users, client, grade_test):

    login_response = client.post("/auth", json={
        "email": "test@gmail.com",
        "password": "12345"
    })
    assert login_response.status_code == 200

    response = client.get("/grade/me")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0

    first_grade = data[0]
    assert first_grade["kind"] == "grade"
    assert first_grade["value"] == 4
    
    
