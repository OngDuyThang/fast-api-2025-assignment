import email
import re
from datetime import datetime
from typing import Optional
from uuid import UUID as NativeUUID

from models.task import TaskDto
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateUserDto(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    email: Optional[str] = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Password must contain at least one uppercase letter, one lowercase letter, and one number",
    )
    company_id: Optional[NativeUUID] = Field(default=None)

    @field_validator("password")
    def validate_password(cls, value):
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$", value):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, and one number"
            )
        return value

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "Password1",
            }
        },
    )


class UpdateUserDto(BaseModel):
    first_name: Optional[str] = Field(min_length=1, max_length=100)
    last_name: Optional[str] = Field(min_length=1, max_length=100)

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
            }
        },
    )


class UserDto(BaseModel):
    id: NativeUUID
    username: str = Field(min_length=1, max_length=100)
    email: Optional[str] = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    company_id: Optional[NativeUUID]
    tasks: list[TaskDto] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
