from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart import Cart
from app.schemas.cart import CartItemCreate, CartItemOut
from app.auth.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])

@router.post("/", response_model=CartItemOut)
async def add_to_cart(
    item: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = Cart(user_id=current_user.id, **item.dict())
    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return cart_item

@router.get("/", response_model=list[CartItemOut])
async def get_my_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    return result.scalars().all()
