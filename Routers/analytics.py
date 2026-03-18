from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

import crud
import model
from database import SessionLocal

router = APIRouter(prefix="/analytics")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    user_id: int = Header()
):
    admin = db.query(model.User).filter(model.User.id == user_id).first()
    if admin.role != "admin":
        return []
    users = db.query(model.User).all()
    return [{"id": u.id, "username": u.username} for u in users]

@router.get("/")
def get_analytics(
    db: Session = Depends(get_db),
    user_id: int = Header(),
    target_user_id: int = Header(default=None)
):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    
    # (if admin selected a specific user)
    if user.role == "admin" and target_user_id:
        target = db.query(model.User).filter(model.User.id == target_user_id).first()
        return crud.get_analytics(db, target)
    
    return crud.get_analytics(db, user)