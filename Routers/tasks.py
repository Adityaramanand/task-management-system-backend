from http.client import HTTPException

from fastapi import APIRouter, Depends ,Header,Query
from sqlalchemy.orm import Session

import crud
import schema
import model
from database import SessionLocal


router = APIRouter(prefix="/tasks")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session, user_id: int = Header()):
    return db.query(model.User).filter(model.User.id == user_id).first()


@router.get("")
def get_tasks(
    db: Session = Depends(get_db),
    user_id: int = Header(),
    selected_user_id: int = Query(None)
):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user.role == "admin" and selected_user_id:
        target_user = db.query(model.User).filter(model.User.id == selected_user_id).first()
        return crud.get_tasks(db, target_user)
    return crud.get_tasks(db, user)

@router.post("")
def create_task(
    task: schema.TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Header()
):

    user = db.query(model.User).filter(model.User.id == user_id).first()

    return crud.create_task(db, task, user)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Header()
):

    user = db.query(model.User).filter(model.User.id == user_id).first()

    return crud.delete_task(db, task_id, user)

# @router.put("/tasks/{task_id}")
# def update_task(task_id: int, task: schema.TaskUpdate, db: Session = Depends(get_db)):

#     return crud.update_task(db, task_id, task)

@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: schema.TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Header()
):

    user = db.query(model.User).filter(model.User.id == user_id).first()

    updated_task = crud.update_task(db, task_id, task, user)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task