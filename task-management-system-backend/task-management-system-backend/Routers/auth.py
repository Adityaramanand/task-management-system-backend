from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schema
import model
from auth_utils import create_access_token, get_current_user, get_db

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "id":   db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type":   "bearer",
        "id":           db_user.id,
        "username":     db_user.username,
        "email":        db_user.email,
        "role":         db_user.role
    }


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # ← JWT auth
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    users = db.query(model.User).filter(model.User.role != "admin").all()
    return [{"id": u.id, "username": u.username} for u in users]