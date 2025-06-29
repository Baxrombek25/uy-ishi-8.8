from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.order import Order
from app.models.cart import Cart
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderOut
from app.auth.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
async def place_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart_items = result.scalars().all()
    if not cart_items:
        raise HTTPException(400, detail="Savatchangiz bo‘sh")

    total = 0
    for item in cart_items:
        prod = await db.get(Product, item.product_id)
        if prod:
            total += (prod.price - prod.discount) * item.quantity

    new_order = Order(
        user_id=current_user.id,
        address=order_data.address,
        total_price=total
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    # cart tozalash
    for item in cart_items:
        await db.delete(item)
    await db.commit()

    return new_order

@router.get("/", response_model=list[OrderOut])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    return result.scalars().all()
