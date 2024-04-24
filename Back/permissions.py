from fastapi import HTTPException, status, Depends

from users import fastapi_users
from models import Roles


current_active_user = fastapi_users.current_user(active=True)


async def read_only_or_higher(user=Depends(current_active_user)):
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def user_or_higher(user=Depends(current_active_user)):
    if user.role in [Roles.USER, Roles.MANAGER, Roles.ADMIN]:
        return user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def manager_or_higher(user=Depends(current_active_user)):
    if user.role == Roles.ADMIN:
        return user

    if user.role == Roles.MANAGER:
        return user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def admin(user=Depends(current_active_user)):
    if user.role == Roles.ADMIN:
        return user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
