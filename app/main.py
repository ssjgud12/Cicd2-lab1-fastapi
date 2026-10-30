from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserRead

app = FastAPI()


@app.post("/api/users", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")
    db.refresh(new_user)
    return new_user


@app.get("/api/users", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/api/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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


def test_delete_user(client): 
    created = client.post( 
        "/api/users", 
        json=user_payload(), 
    ).json() 
 
    user_id = created["id"] 
 
    response = client.delete(f"/api/users/{user_id}") 
    assert response.status_code == 204 
 
    response = client.get(f"/api/users/{user_id}") 
    assert response.status_code == 404 
 
 
def test_delete_missing_user_returns_404(client): 
    response = client.delete("/api/users/999") 
 
    assert response.status_code == 404

@pytest.mark.parametrize( 
    "bad_sid", 
    [ 
        "BAD123", 
        "s1234567", 
        "S123", 
        "S12345678", 
    ], 
) 
def test_invalid_student_id_returns_422(client, bad_sid): 
    response = client.post( 
        "/api/users", 
        json=user_payload(sid=bad_sid), 
    ) 
 
    assert response.status_code == 422