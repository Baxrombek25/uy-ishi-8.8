from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import ReviewCreate, ReviewOut
from app.auth.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewOut)
async def create_review(
    data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = await db.get(Product, data.product_id)
    if not product:
        raise HTTPException(404, detail="Mahsulot topilmadi")
    
    review = Review(**data.dict(), user_id=current_user.id)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

@router.get("/product/{product_id}", response_model=list[ReviewOut])
async def get_reviews(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.product_id == product_id))
    return result.scalars().all()
