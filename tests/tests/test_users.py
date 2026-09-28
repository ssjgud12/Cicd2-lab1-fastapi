import pytest

def user_payload( 
    uid=1, 
    name="Alvin", 
    email="Alvin@atu.ie", 
    age=25, 
    student_id="S1234567", 
): 
    return { 
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
def test_bad_student_id_returns_422(cilent, bad_student_id):
    response = cilent.post(
        "/api/users",
        json=user_payload(uid=3, student_id=bad_student_id),
    )

    assert response.status_code == 422

