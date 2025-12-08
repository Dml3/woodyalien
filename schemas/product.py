from pydantic import BaseModel
from typing import List, Optional


class MediaOut(BaseModel):
    id: int
    filename: str

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    title: str
    description: Optional[str]
    media: List[str] = []


class ProductOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    media: List[MediaOut]

    class Config:
        from_attributes = True
