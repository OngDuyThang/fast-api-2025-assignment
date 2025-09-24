from datetime import datetime
from typing import Any

from database import get_db_context
from fastapi import Depends, HTTPException
from models.user import CreateUserDto, UpdateUserDto, UserDto
from schemas.user import User
from services.auth import create_hashed_password
from sqlalchemy.orm import Session, joinedload


def create_user(request: CreateUserDto, db: Session):
    required_fields = [
        request.username,
        request.email,
        request.first_name,
        request.last_name,
        request.password,
    ]
    if not all(required_fields):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        user = (
            db.query(User)
            .filter(
                (User.username == request.username) or (User.email == request.email)
            )
            .first()
        )
        if user:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = {
            **request.__dict__,
            "password": create_hashed_password(request.password),
            "created_at": datetime.now(),
            **({"company_id": request.company_id} if request.company_id else {}),
        }

        new_user = User(**new_user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_user.__delattr__("password")
        return UserDto(**new_user.__dict__)
    except Exception as _:
        raise


def get_users(page: int, limit: int, db: Session):
    try:
        offset = (page - 1) * limit
        return (
            db.query(User).order_by(User.created_at).offset(offset).limit(limit).all()
        )
    except Exception as _:
        raise


def get_user_by_id(user_id: str, db: Session):
    try:
        user = (
            db.query(User)
            .options(joinedload(User.tasks))
            .filter(User.id == user_id)
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserDto(**user.__dict__)
    except Exception as _:
        raise


def update_user(user_id: str, request: UpdateUserDto, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in request.__dict__.items():
            if value:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return UserDto(**user.__dict__)

    except Exception as _:
        raise


def delete_user(user_id: str, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()

        return "Ok"
    except Exception as _:
        raise
