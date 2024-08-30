from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Company
from app.schemas import CompanyResponse, CompanyCreate, CompanyUpdate

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    # Declare model specific CRUD operation methods.

    def get_one_by_name(self, db: Session, name: str) -> Company:
        return db.query(Company).filter(Company.name == name).first()


company = CRUDCompany(Company)

