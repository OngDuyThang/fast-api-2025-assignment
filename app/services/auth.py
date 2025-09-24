from datetime import datetime, timedelta
from tkinter import E
from typing import Any, Optional

from database import get_db_context
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from schemas.user import User
from settings import JWT_ALGORITHM, JWT_SECRET
from sqlalchemy.orm import Session

bcrypt_context = CryptContext(schemes=["bcrypt"])

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_hashed_password(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session):
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credential")
        return user
    except Exception as e:
        raise e


def create_access_token(user: User, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
        "exp": (
            datetime.now() + expires
            if expires
            else datetime.now() + timedelta(minutes=15)
        ),
    }
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )

        user = {
            "username": payload["sub"],
            "id": payload["id"],
            "first_name": payload["first_name"],
            "last_name": payload["last_name"],
            "is_admin": payload["is_admin"],
        }

        if (user["id"] is None) or (user["username"] is None):
            raise HTTPException(status_code=401, detail="Unauthorized")

        return User(**user)
    except Exception as e:
        raise e


def verify_admin(user: User):
    is_admin = user.__getattribute__("is_admin")
    if not is_admin:
        raise HTTPException(status_code=401, detail="Insufficient permissions")


def verify_owner(owner_id: str, user: User):
    if (user.is_admin is False) and (str(user.id) != str(owner_id)):
        raise HTTPException(status_code=401, detail="Unauthorized")
