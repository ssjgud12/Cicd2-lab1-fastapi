import pytest

def user_payload( 
    uid=1, 
    name="Alvin", 
    email="Alvin@atu.ie", 
    age=25, 
    student_id="S1234567", 
): 
    return 
{ 
        "userid": uid, 
        "name": name, 
        "email": email, 
        "age": age, 
        "student_id": student_id, 
    } 

@pytest.mark.parametrize(
    "bad_student_id",
    ["1234567", "s1234567", "S123" ,"S12345678"],
)
def test_bad_student_id_returns_422(client, bad_student_id): # Fixed typo
    response = client.post(
        "/api/users",
        json=user_payload(uid=3, student_id=bad_student_id),
    )
    assert response.status_code == 422

def test_get_users_returns_created_users(client): 
    client.post("/api/users", json=user_payload(uid=10, name="Alice", email="alice@atu.ie")) 
    response = client.get("/api/users") 
    assert response.status_code == 200 
    data = response.json() 
    assert len(data) == 1 
    assert data[0]["userid"] == 10 
    assert data[0]["name"] == "Alice"

def test_get_existing_user_returns_200(client): 
    client.post("/api/users", json=user_payload(uid=11)) 
    response = client.get("/api/users/11") 
    assert response.status_code == 200 
    assert response.json()["userid"] == 11 # Fixed key name

def test_get_missing_user_returns_404(client): 
    response = client.get("/api/users/999") 
    assert response.status_code == 404 
    assert response.json()["detail"] == "User not found"

def test_delete_existing_user_returns_204(client): 
    client.post("/api/users", json=user_payload(uid=20)) 
    response = client.delete("/api/users/20") 
    assert response.status_code == 204 
    assert response.content == b''

def test_delete_missing_user_returns_404(client): # Fixed typo
    response = client.delete("/api/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"