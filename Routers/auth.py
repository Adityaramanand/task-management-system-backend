from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schema
from database import SessionLocal
import model
from fastapi import Header

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
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role
    }
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    user_id: int = Header()
):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    users = db.query(model.User).filter(model.User.role != "admin").all()
    return [{"id": u.id, "username": u.username} for u in users]