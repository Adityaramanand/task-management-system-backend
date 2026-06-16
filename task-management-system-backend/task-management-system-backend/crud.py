from sqlalchemy.orm import Session
import model
import schema
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------- USER ----------

def create_user(db: Session, user: schema.UserCreate):
    from auth_utils import hash_password
    db_user = model.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password), 
        role="user"   # (default role)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db: Session, user: schema.UserLogin):
    from auth_utils import verify_password
    db_user = db.query(model.User).filter(
        model.User.email == user.email
    ).first()
    if not db_user:
        return None
    if not verify_password(user.password, db_user.password):
        return None
    return db_user


# ---------- TASKS ----------

def get_tasks(db: Session, user):

    if user.role == "admin":
        tasks = db.query(model.Task).all()
    else:
        tasks = db.query(model.Task).filter(
            model.Task.user_id == user.id
        ).all()

    result = []
    for task in tasks:
        owner = db.query(model.User).filter(model.User.id == task.user_id).first()
        result.append({
            "id":           task.id,
            "title":        task.title,
            "description":  task.description,
            "priority":     task.priority,
            "status":       task.status,
            "created_at":   task.created_at,
            "due_date":     task.due_date,
            "completed_at": task.completed_at,
            "user_id":      task.user_id,
            "owner_name":   owner.username if owner else "-"
        })

    return result


def create_task(db: Session, task: schema.TaskCreate, user):

    db_task = model.Task(
        **task.model_dump(),
        user_id=user.id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int, user):

    task = db.query(model.Task).filter(
        model.Task.id == task_id
    ).first()

    if not task:
        return None

    if user.role != "admin" and task.user_id != user.id:
        return None

    db.delete(task)
    db.commit()

    return task

def update_task(db, task_id, task, user):

    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()

    if not db_task:
        return None
 
    if user.role != "admin" and db_task.user_id != user.id:
        return None
  
    db_task.title = task.title
    db_task.description = task.description
    db_task.priority = task.priority
    db_task.due_date = task.due_date

    new_status = task.status
    db_task.status = new_status


    if new_status == "pending" and db_task.started_at is None:
        db_task.started_at = datetime.now()

    if new_status == "completed":
        db_task.completed_at = datetime.now()

    db.commit()
    db.refresh(db_task)

    return db_task

# ---------- TASK ANALYTICS ----------
def get_task_analytics(db, user):

    if user.role == "admin":
        tasks = db.query(model.Task).all()
    else:
        tasks = db.query(model.Task).filter(
            model.Task.user_id == user.id
        ).all()

    if not tasks:
        return {
            "total_tasks":0,
            "completed":0,
            "pending":0,
            "tasks_per_day":{}
        }

    df = pd.DataFrame([{
        "status":t.status,
        "created_at":t.created_at,
        "user_id":t.user_id
    } for t in tasks])

    total_tasks = len(df)

    completed = np.sum(df["status"] == "completed")

    pending = np.sum(df["status"] != "completed")

    df["date"] = pd.to_datetime(df["created_at"]).dt.date

    tasks_per_day = df.groupby("date").size().to_dict()

    # ---------- matplotlib charts ----------

    plt.figure()

    plt.pie(
        [completed,pending],
        labels=["Completed","Pending"],
        autopct="%1.1f%%"
    )

    plt.title("Task Status")

    plt.savefig("task_status_chart.png")

    plt.close()

    plt.figure()

    plt.bar(tasks_per_day.keys(),tasks_per_day.values())

    plt.title("Tasks Per Day")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("tasks_per_day_chart.png")

    plt.close()

    return {
        "total_tasks":int(total_tasks),
        "completed":int(completed),
        "pending":int(pending),
        "tasks_per_day":tasks_per_day
    }
# ---------- ANALYTICS ----------

def get_analytics(db: Session, user):

    if user.role == "admin":
        total       = db.query(model.Task).count()
        completed   = db.query(model.Task).filter(model.Task.status == "completed").count()
        pending     = db.query(model.Task).filter(model.Task.status == "pending").count()
        in_progress = db.query(model.Task).filter(model.Task.status == "in_progress").count()
        not_started = db.query(model.Task).filter(model.Task.status == "not_started").count()
    else:
        total       = db.query(model.Task).filter(model.Task.user_id == user.id).count()
        completed   = db.query(model.Task).filter(model.Task.user_id == user.id, model.Task.status == "completed").count()
        pending     = db.query(model.Task).filter(model.Task.user_id == user.id, model.Task.status == "pending").count()
        in_progress = db.query(model.Task).filter(model.Task.user_id == user.id, model.Task.status == "in_progress").count()
        not_started = db.query(model.Task).filter(model.Task.user_id == user.id, model.Task.status == "not_started").count()

    # Priority breakdown for bar chart
    priorities = ["low", "medium", "high"]
    statuses   = ["not_started", "pending", "in_progress", "completed"]

    priority_breakdown = {}
    for p in priorities:
        priority_breakdown[p] = {}
        for s in statuses:
            priority_breakdown[p][s] = db.query(model.Task).filter(
                model.Task.priority == p,
                model.Task.status == s
            ).count()

    # Tasks per day — grouped by DATE only (fixes giant single-bar bug)
    from sqlalchemy import func, cast, Date

    if user.role == "admin":
        daily = db.query(
            cast(model.Task.created_at, Date).label("date"),
            func.count().label("count")
        ).group_by(cast(model.Task.created_at, Date)).all()
    else:
        daily = db.query(
            cast(model.Task.created_at, Date).label("date"),
            func.count().label("count")
        ).filter(
            model.Task.user_id == user.id
        ).group_by(cast(model.Task.created_at, Date)).all()

    tasks_per_day = {str(row.date): row.count for row in daily}

    return {
        "total_tasks":        total,
        "completed":          completed,
        "pending":            pending,
        "in_progress":        in_progress,
        "not_started":        not_started,
        "priority_breakdown": priority_breakdown,
        "tasks_per_day":      tasks_per_day
    }