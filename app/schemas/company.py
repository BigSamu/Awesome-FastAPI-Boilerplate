from typing import Optional

from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    type: str

class CompanyUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]

class CompanyResponse(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True
