from pydantic import BaseModel
from typing import List, Optional


class BlogCreate(BaseModel):
    title: str
    description: Optional[str]
    media: List[str] = []


class BlogOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    media: List[str]

    class Config:
        from_attributes = True
