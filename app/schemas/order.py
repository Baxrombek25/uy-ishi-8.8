from pydantic import BaseModel
from enum import Enum

class OrderCreate(BaseModel):
    address: str

class OrderOut(BaseModel):
    id: int
    user_id: int
    address: str
    total_price: float
    payment_status: str
    status: str

    class Config:
        orm_mode = True
