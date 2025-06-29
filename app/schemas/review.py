from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = None
    product_id: int

class ReviewOut(BaseModel):
    id: int
    rating: int
    comment: str | None
    user_id: int
    product_id: int

    class Config:
        orm_mode = True
