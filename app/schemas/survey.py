from typing import Optional, Dict

from pydantic import BaseModel


class PostCreate(BaseModel):
    filename: str
    image_url: str
    provider: str
    location: str
    reference_number: str


class PostUpdate(BaseModel):
    filename: Optional[str]
    image_url: Optional[str]
    provider: Optional[str]
    location: Optional[str]
    reference_number: Optional[str]


class PostResponse(BaseModel):
    id: int
    filename: str
    image_url: str
    provider: str
    location: str
    reference_number: str

    class Config:
        from_attributes = True


class PostLoadDataResponse(BaseModel):
    details: PostResponse
    metadata: Optional[Dict[str, str]] = {}

    class Config:
        from_attributes = True
