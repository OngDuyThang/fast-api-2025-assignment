from datetime import timedelta

from database import get_db_context
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import authenticate_user, create_access_token, create_hashed_password
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_context),
):
    user = authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    token = create_access_token(user=user, expires=timedelta(minutes=120))

    return {
        "access_token": token,
        "token_type": "bearer",
    }
