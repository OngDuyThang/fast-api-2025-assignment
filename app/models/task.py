from datetime import datetime
from typing import Optional
from uuid import UUID as NativeUUID

from common.enums import TaskPriority, TaskStatus
from pydantic import BaseModel, ConfigDict, Field


class CreateTaskDto(BaseModel):
    summary: Optional[str] = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(min_length=1, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.BACKLOG)
    priority: TaskPriority = Field(default=TaskPriority.LOW)

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "summary": "Task summary",
                "description": "Task description",
                "status": "backlog",
                "priority": "low",
            }
        },
    )


class UpdateTaskDto(BaseModel):
    summary: Optional[str] = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(min_length=1, max_length=500)
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "summary": "Task summary",
                "description": "Task description",
                "status": "backlog",
                "priority": "low",
            }
        },
    )


class TaskDto(BaseModel):
    id: NativeUUID
    summary: Optional[str]
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    owner_id: Optional[NativeUUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
