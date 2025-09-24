from datetime import datetime
from typing import Optional
from uuid import UUID as NativeUUID

from common.enums import CompanyMode
from models.user import UserDto
from pydantic import BaseModel, ConfigDict, Field


class CreateCompanyDto(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str]
    mode: Optional[CompanyMode] = Field(default=CompanyMode.OUTSOURCE)
    rating: Optional[float] = Field(default=0, ge=0, le=5)

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Company Name",
                "description": "Company Description",
                "mode": "outsource",
                "rating": 4.5,
            }
        },
    )


class UpdateCompanyDto(BaseModel):
    description: Optional[str]
    mode: Optional[CompanyMode]

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {"description": "Company Description", "mode": "outsource"}
        },
    )


class CompanyDto(BaseModel):
    id: NativeUUID
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str]
    mode: CompanyMode
    rating: Optional[float] = Field(ge=0, le=5)
    employees: list[UserDto] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        from_attributes = True
