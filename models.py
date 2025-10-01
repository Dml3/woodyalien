from pydantic import BaseModel
from typing import List

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    images: List[str]

    class Config:
        orm_mode = True
