from datetime import datetime

from fastapi import HTTPException
from models.task import CreateTaskDto, TaskDto, UpdateTaskDto
from schemas.task import Task
from schemas.user import User
from sqlalchemy.orm import Session


def create_task(request: CreateTaskDto, user: User, db: Session):
    required_fields = [
        request.summary,
        request.description,
        request.status,
        request.priority,
    ]
    if not all(required_fields):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        new_task = {
            **request.__dict__,
            "owner_id": user.id,
            "created_at": datetime.now(),
        }
        new_task = Task(**new_task)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return TaskDto(**new_task.__dict__)

    except Exception as _:
        raise


def get_tasks(page: int, limit: int, user: User, db: Session):
    try:
        offset = (page - 1) * limit
        query = db.query(Task)

        if user.is_admin is False:
            query = query.filter(Task.owner_id == user.id)

        return query.order_by(Task.created_at).offset(offset).limit(limit).all()
    except Exception as _:
        raise


def get_task_by_id(task_id: str, user: User, db: Session):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if (user.is_admin is False) and (str(task.owner_id) != str(user.id)):
            raise HTTPException(
                status_code=403, detail="User is not owner of this task"
            )

        return TaskDto(**task.__dict__)
    except Exception as _:
        raise


def update_task(
    task_id: str,
    request: UpdateTaskDto,
    user: User,
    db: Session,
):
    try:
        task = (
            db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        for key, value in request.__dict__.items():
            if value:
                setattr(task, key, value)

        db.add(task)
        db.commit()
        db.refresh(task)

        return TaskDto(**task.__dict__)
    except Exception as _:
        raise


def delete_task(task_id: str, user: User, db: Session):
    try:
        task = (
            db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(task)
        db.commit()

        return "Ok"
    except Exception as _:
        raise
