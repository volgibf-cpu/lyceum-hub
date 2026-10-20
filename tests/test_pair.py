import pytest

def test_pair(test_users, auth_student, test_pair):

    response = auth_student.get("/pair/")

    assert response.status_code == 200

    data = response.json()

    pair_info = data[0]

    assert len(data) > 0
    assert pair_info["teacher"]