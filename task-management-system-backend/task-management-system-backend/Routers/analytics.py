from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import crud
import model
from auth_utils import get_current_user, get_db

router = APIRouter(prefix="/analytics")


@router.get("/")
def get_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),  # ← JWT auth
    selected_user_id: int = Query(None)
):
    if current_user.role == "admin" and selected_user_id:
        target_user = db.query(model.User).filter(
            model.User.id == selected_user_id
        ).first()
        return crud.get_analytics(db, target_user)
    return crud.get_analytics(db, current_user)