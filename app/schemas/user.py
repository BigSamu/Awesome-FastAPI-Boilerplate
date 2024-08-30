from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas import CompanyResponse


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    company_id: int


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    company_id: Optional[int]


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    company: CompanyResponse

    class Config:
        from_attributes = True
