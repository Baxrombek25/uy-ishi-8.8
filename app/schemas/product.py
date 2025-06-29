from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    discount: Optional[float] = 0
    stock: int
    image: Optional[str] = None
    category_id: int

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    discount: float
    stock: int
    image: Optional[str]
    category_id: int

    class Config:
        orm_mode = True
