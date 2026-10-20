import pytest
from datetime import date

def test_set_grade(test_users, auth_teacher):
  
    response = auth_teacher.post("/grade/set", json={
        "student_id": test_users["student"].id,
        "subject_name": "Математика",
        "kind": "grade",
        "value": 4,
        "status": None,
        "date": "2026-10-19",
        "comment": None
    })


    assert response.status_code == 200
    assert response.json()["message"] == "Оценка успешно выставлена!"


def test_get_students_grades(grade_test, test_users, auth_teacher):

    response = auth_teacher.get("/grade/group")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1

    assert any(str(g["student_id"]) == str(test_users["student"].id) for g in data)
    

def test_student_grades(test_users, auth_teacher, grade_test):

    response = auth_teacher.get("/grade/student", params={"user_id": test_users["student"].id})
    assert response.status_code == 200

    data = response.json()

    grade = data[0]
    assert grade["student"] != "—"
    assert grade["teacher"] != "—"

    

def test_my_grades(test_users, auth_student, grade_test):

    response = auth_student.get("/grade/me")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0

    first_grade = data[0]
    assert first_grade["kind"] == "grade"
    assert first_grade["value"] == 4
    
    
def test_student_role(test_users, auth_student, grade_test):

    response = auth_student.post("/grade/set", json={
        "subject_name": "Математика",
        "student_id": test_users["student"].id,
        "date": "2026-10-03",
        "kind": "grade",
        "value": 5
    })

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"