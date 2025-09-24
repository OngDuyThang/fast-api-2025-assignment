import services.user as user_service
from database import get_db_context
from fastapi import APIRouter, Depends, HTTPException, Query
from models.user import CreateUserDto, UpdateUserDto, UserDto
from services.auth import token_interceptor, verify_admin, verify_owner
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(prefix="/users", tags=["User"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDto,
    description="""##
    - Admin can create user
    - Normal user can not create user""",
)
async def create_user(
    request: CreateUserDto, user=Depends(token_interceptor), db=Depends(get_db_context)
):
    verify_admin(user)
    return user_service.create_user(request, db)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserDto],
    description="""##
    - Admin can get all users
    - Normal user can not get all users""",
)
async def get_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    user=Depends(token_interceptor),
    db=Depends(get_db_context),
):
    verify_admin(user)
    return user_service.get_users(page, limit, db)


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDto,
    description="""##
    - Admin can get any user
    - Normal user can get their user""",
)
async def get_user_by_id(
    user_id: str,
    user=Depends(token_interceptor),
    db=Depends(get_db_context),
):
    verify_owner(user_id, user)
    return user_service.get_user_by_id(user_id, db)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDto,
    description="""##
    - Admin can update any user
    - Normal user can update their user""",
)
async def update_user(
    user_id: str,
    request: UpdateUserDto,
    user=Depends(token_interceptor),
    db=Depends(get_db_context),
):
    verify_owner(user_id, user)
    return user_service.update_user(user_id, request, db)


@router.delete(
    "/{user_id}",
    description="""##
    - Admin can delete any user
    - Normal user can not delete user""",
)
async def delete_user(
    user_id: str, user=Depends(token_interceptor), db: Session = Depends(get_db_context)
):
    verify_admin(user)
    return user_service.delete_user(user_id, db)
