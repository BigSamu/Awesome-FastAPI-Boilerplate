from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_db, get_current_user


router = APIRouter()


@router.get("", response_model=List[schemas.CompanyResponse])
def read_all_companies(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve all companies.
    """
    companies = crud.company.get_all(db)
    return companies

@router.get("/{company_id}", response_model=schemas.CompanyResponse)
def read_one_company(company_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve one company by id.
    """
    company = crud.company.get_one(db, model_id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The company with id '{company_id}' does not exist in the database.",
        )
    return company

@router.post("", response_model=schemas.CompanyResponse)
def create_company(*, db: Session = Depends(get_db), company_in: schemas.CompanyCreate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Create new company.
    """
    company =  crud.company.get_one_by_name(db,name=company_in.name)
    if company:
          raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Company already exist in database.",
        )
    company = crud.company.create(db, obj_in=company_in)
    
    return company

@router.put("/{company_id}", response_model=schemas.CompanyResponse)
def update_company(*, company_id: int, db: Session = Depends(get_db), company_in: schemas.CompanyUpdate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Update one company by id.
    """
    company = crud.company.get_one(db, model_id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The company with id '{company_id}' does not exist in the database.",
        )
    company = crud.company.update(db, db_obj=company, obj_in=company_in)

    return company

@router.delete("", response_model=schemas.Message)
def delete_all_companies(*, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete all companies.
    """
    companies = crud.company.get_all(db)
    if not companies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"It doesn't exist any company in the database.",
        )
    rows_deleted = crud.company.remove_all(db)
    return {"message": f"{rows_deleted} companies were deleted."}

@router.delete("/{company_id}", response_model=schemas.Message)
def delete_one_company(*, company_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete one company by id.
    """
    company = crud.company.get_one(db, model_id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The company with id '{company_id}' does not exist in the database.",
        )
    crud.company.remove_one(db, model_id=company.id)
    return {"message": f"The company with id '{company_id}' deleted."}