import services.task as task_service
from database import get_db_context
from fastapi import APIRouter, Depends, HTTPException, Query
from models.task import CreateTaskDto, TaskDto, UpdateTaskDto
from services.auth import token_interceptor
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(prefix="/tasks", tags=["Task"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskDto,
    description="""##
    - Admin can not create task for others
    - User create task for themselves""",
)
def create_task(
    request: CreateTaskDto,
    user=Depends(token_interceptor),
    db: Session = Depends(get_db_context),
):
    return task_service.create_task(request, user, db)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskDto],
    description="""##
    - Admin can get all tasks
    - Normal user can get their tasks""",
)
def get_tasks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    user=Depends(token_interceptor),
    db: Session = Depends(get_db_context),
):
    return task_service.get_tasks(page, limit, user, db)


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskDto,
    description="""##
    - Admin can get any task
    - Normal user can get their task""",
)
def get_task_by_id(
    task_id: str, user=Depends(token_interceptor), db: Session = Depends(get_db_context)
):
    return task_service.get_task_by_id(task_id, user, db)


@router.put(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskDto,
    description="""##
    - Admin can not update others task
    - User can update their task""",
)
def update_task(
    task_id: str,
    request: UpdateTaskDto,
    user=Depends(token_interceptor),
    db: Session = Depends(get_db_context),
):
    return task_service.update_task(task_id, request, user, db)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    description="""##
    - Admin can not delete others task
    - User can delete their task""",
)
def delete_task(
    task_id: str, user=Depends(token_interceptor), db: Session = Depends(get_db_context)
):
    return task_service.delete_task(task_id, user, db)
