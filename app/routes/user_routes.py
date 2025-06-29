from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserOut, UserUpdate
from app.auth.deps import get_current_user, get_db
from app.models.user import User
from app.utils.security import hash_password

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_profile(
    update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if update.username:
        current_user.username = update.username
    if update.password:
        current_user.hashed_password = hash_password(update.password)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
