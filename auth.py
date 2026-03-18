from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schema
from database import SessionLocal

router = APIRouter(prefix="/auth")


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register(user: schema.UserCreate, db: Session = Depends(get_db)):

    return crud.create_user(db, user)


@router.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):

    db_user = crud.login_user(db, user)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    }