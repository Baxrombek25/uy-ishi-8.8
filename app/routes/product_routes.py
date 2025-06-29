from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut
from app.auth.deps import get_db

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

@router.post("/", response_model=ProductOut)
async def create_product(prod: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**prod.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[ProductOut])
async def list_products(
    search: str = Query(None, description="Nomi bo‘yicha izlash"),
    category_id: int = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    in_stock: bool = Query(None),
    sort_by: str = Query(None, enum=["price", "name", "stock"]),
    db: AsyncSession = Depends(get_db)
):
    query = select(Product)

    filters = []
    if search:
        filters.append(Product.name.ilike(f"%{search}%"))
    if category_id:
        filters.append(Product.category_id == category_id)
    if min_price is not None:
        filters.append(Product.price >= min_price)
    if max_price is not None:
        filters.append(Product.price <= max_price)
    if in_stock is not None:
        if in_stock:
            filters.append(Product.stock > 0)
        else:
            filters.append(Product.stock <= 0)

    if filters:
        query = query.where(and_(*filters))

    if sort_by == "price":
        query = query.order_by(Product.price)
    elif sort_by == "name":
        query = query.order_by(Product.name)
    elif sort_by == "stock":
        query = query.order_by(Product.stock)

    result = await db.execute(query)
    return result.scalars().all()
