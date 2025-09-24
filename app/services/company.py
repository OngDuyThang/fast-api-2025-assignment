from datetime import datetime
from math import e

from fastapi import HTTPException
from models.company import CompanyDto, CreateCompanyDto, UpdateCompanyDto
from models.user import UserDto
from schemas.company import Company
from schemas.user import User
from sqlalchemy.orm import Session, joinedload


def create_company(request: CreateCompanyDto, db: Session):
    required_fields = [request.name, request.mode]
    if not all(required_fields):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        company = db.query(Company).filter(Company.name == request.name).first()
        if company:
            raise HTTPException(status_code=400, detail="Company already exists")

        new_company = {**request.__dict__, "created_at": datetime.now()}
        new_company = Company(**new_company)

        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        return CompanyDto(**new_company.__dict__)
    except Exception as _:
        raise


def get_companies(page: int, limit: int, db: Session):
    try:
        offset = (page - 1) * limit
        return (
            db.query(Company)
            .order_by(Company.created_at)
            .offset(offset)
            .limit(limit)
            .all()
        )
    except Exception as _:
        raise


def get_company_by_id(company_id: str, user: User, db: Session):
    try:
        company = (
            db.query(Company)
            .options(joinedload(Company.employees))
            .filter(Company.id == company_id)
            .first()
        )
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        if (user.is_admin is True) or any(
            str(user.id) == str(employee.id) for employee in company.employees
        ):
            return CompanyDto(**company.__dict__)

        raise HTTPException(status_code=403, detail="User is not in this company")

    except Exception as _:
        raise


def update_company(
    company_id: str,
    request: UpdateCompanyDto,
    db: Session,
):
    required_fields = [request.description, request.mode]
    if not all(required_fields):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        for key, value in request.__dict__.items():
            if value:
                setattr(company, key, value)

        db.add(company)
        db.commit()
        db.refresh(company)

        return CompanyDto(**company.__dict__)
    except Exception as _:
        raise


def delete_company(company_id: str, db: Session):
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        db.delete(company)
        db.commit()

        return "Ok"
    except Exception as _:
        raise
