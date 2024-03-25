from models import Roles
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status
from fastapi import Depends
from users import fastapi_users
from db.engine import get_async_session
from models import User

current_active_user = fastapi_users.current_user(active=True)


async def read_only_or_higher(user=Depends(current_active_user)):
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def user_or_higher(user=Depends(current_active_user)):
    if user.role in [Roles.USER, Roles.MANAGER, Roles.ADMIN]:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def manager_or_higher(
    user=Depends(current_active_user)
):
    if user.role == Roles.ADMIN:
        return user
    if user.role == Roles.MANAGER:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def admin(user=Depends(current_active_user)):
    if user.role == Roles.ADMIN:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
