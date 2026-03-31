from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schema
import model
from auth_utils import get_current_user, get_db

router = APIRouter(prefix="/tasks")


@router.get("")
def get_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),  # ← JWT auth
    selected_user_id: int = Query(None)
):
    if current_user.role == "admin" and selected_user_id:
        target_user = db.query(model.User).filter(
            model.User.id == selected_user_id
        ).first()
        return crud.get_tasks(db, target_user)
    return crud.get_tasks(db, current_user)


@router.post("")
def create_task(
    task: schema.TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # ← JWT auth
):
    return crud.create_task(db, task, current_user)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # ← JWT auth
):
    return crud.delete_task(db, task_id, current_user)


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: schema.TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # ← JWT auth
):
    updated_task = crud.update_task(db, task_id, task, current_user)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task