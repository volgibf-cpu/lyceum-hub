import pytest 

def test_auth(test_users, client):
    response = client.post("/auth", json={
        "email": "test@gmail.com",
        "password": "12345"
    })

    assert response.status_code == 200
    assert response.json()["message"] is not None

def test_user_not_found(test_users, client):
    response = client.post("/auth", json={
        "email": "wrong@gmail.com",
        "password": "12345"
    })

    assert response.status_code == 401
    assert response.json()['detail'] == "Invalid credentials"