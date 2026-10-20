import pytest 

def test_user_profile(test_users, auth_student):

    response = auth_student.get("/users/me")

    assert response.status_code == 200
    assert response.json()["group"] 

def test_get_student(test_users, auth_teacher):

    response = auth_teacher.get("/users/student", params={"group_name": "TestGroup"})

    assert response.status_code == 200

    check_data = response.json()

    assert len(check_data) > 0
