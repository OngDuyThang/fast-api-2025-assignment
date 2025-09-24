import services.company as company_service
from database import get_db_context
from fastapi import APIRouter, Depends, HTTPException, Query
from models.company import CompanyDto, CreateCompanyDto, UpdateCompanyDto
from services.auth import token_interceptor, verify_admin
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(prefix="/companies", tags=["Company"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyDto)
def create_company(
    request: CreateCompanyDto,
    user=Depends(token_interceptor),
    db: Session = Depends(get_db_context),
):
    verify_admin(user)
    return company_service.create_company(request, db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CompanyDto])
def get_companies(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    user=Depends(token_interceptor),
    db=Depends(get_db_context),
):
    verify_admin(user)
    return company_service.get_companies(page, limit, db)


@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyDto)
def get_company_by_id(
    company_id: str,
    user=Depends(token_interceptor),
    db: Session = Depends(get_db_context),
):
    return company_service.get_company_by_id(company_id, user, db)


@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyDto)
def update_company(
    company_id: str,
    request: UpdateCompanyDto,
    user=Depends(token_interceptor),
    db: Session = Depends(get_db_context),
):
    verify_admin(user)
    return company_service.update_company(company_id, request, db)


@router.delete("/{company_id}", status_code=status.HTTP_200_OK)
def delete_company(
    company_id: str,
    user=Depends(token_interceptor),
    db: Session = Depends(get_db_context),
):
    verify_admin(user)
    return company_service.delete_company(company_id, db)
