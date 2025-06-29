from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.deps import get_db, admin_required
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.schemas.order import OrderOut
from app.schemas.user import UserOut
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

@router.get("/orders", response_model=list[OrderOut])
async def get_all_orders(db: AsyncSession = Depends(get_db), admin=Depends(admin_required)):
    result = await db.execute(select(Order))
    return result.scalars().all()

@router.put("/orders/{order_id}/status", response_model=OrderOut)
async def update_order_status(order_id: int, status: OrderStatus, db: AsyncSession = Depends(get_db), admin=Depends(admin_required)):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(404, detail="Buyurtma topilmadi")
    order.status = status
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

@router.get("/users", response_model=list[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db), admin=Depends(admin_required)):
    result = await db.execute(select(User))
    return result.scalars().all()



@router.get("/stats")
async def get_statistics(db: AsyncSession = Depends(get_db), admin=Depends(admin_required)):
    today = datetime.utcnow()
    last_7_days = today - timedelta(days=7)

    user_count = await db.execute(select(func.count(User.id)))
    user_total = user_count.scalar()

    order_count = await db.execute(select(func.count(Order.id)))
    order_total = order_count.scalar()

    sales_sum = await db.execute(select(func.sum(Order.total_price)))
    total_sales = sales_sum.scalar() or 0

    recent_orders = await db.execute(
        select(func.count(Order.id)).where(Order.created_at >= last_7_days)
    )
    recent_order_count = recent_orders.scalar()

    return {
        "total_users": user_total,
        "total_orders": order_total,
        "total_sales": total_sales,
        "recent_orders_7_days": recent_order_count
    }
