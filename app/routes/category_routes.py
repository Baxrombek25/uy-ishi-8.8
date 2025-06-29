from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.auth.deps import get_db

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])

@router.post("/", response_model=CategoryOut)
async def create_category(cat: CategoryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.name == cat.name))
    if result.scalar():
        raise HTTPException(400, detail="Category already exists")
    new_cat = Category(name=cat.name)
    db.add(new_cat)
    await db.commit()
    await db.refresh(new_cat)
    return new_cat

@router.get("/", response_model=list[CategoryOut])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()
