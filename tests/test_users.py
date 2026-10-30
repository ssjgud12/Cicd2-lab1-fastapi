import pytest

def user_payload( 
    name="Paul", 
    email="paul@atu.ie", 
    age=25, 
    sid="S1234567", 
): 
    return { 
        "name": name, 
        "email": email, 
        "age": age, 
        "student_id": sid, 
    }

def test_get_users(client): 
    client.post("/api/users", json=user_payload()) 
 
    response = client.get("/api/users") 
 
    assert response.status_code == 200 
    assert len(response.json()) == 1 
    assert response.json()[0]["student_id"] == "S1234567" 
 
 
def test_get_user_by_id(client): 
    created = client.post( 
        "/api/users", 
        json=user_payload(), 
    ).json() 
 
    user_id = created["id"] 
    response = client.get(f"/api/users/{user_id}") 
 
    assert response.status_code == 200 
    assert response.json()["email"] == "paul@atu.ie" 
 
 
def test_get_missing_user_returns_404(client): 
    response = client.get("/api/users/999") 
 
    assert response.status_code == 404 
    assert "not found" in response.json()["detail"].lower()

