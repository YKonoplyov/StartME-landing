from typing import Any, AsyncGenerator, Dict, List
from fastapi import Depends
from fastapi_users import IntegerIDMixin, exceptions
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

import models
from db.engine import get_async_session
from models import User


class UsersDB(SQLAlchemyUserDatabase):

    async def get(self, user_id: int) -> User:
        user_statement = (
            select(User).where(User.id == user_id).options(selectinload(User.founds))
        )
        user = await self.session.scalar(user_statement)
        return user

    async def update(self, user: User, update_dict: Dict[str, Any]) -> User:
        found_ids = update_dict.get("foudns_ids")
        if found_ids:
            founds_statement = select(models.Found).where(
                models.Found.id.in_(found_ids)
            )
            founds = self.session.scalars(founds_statement)
            for found in founds:
                user.founds.append(found)

        for key, value in update_dict.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_username(self, username: str):
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        user = await self._get_user(statement)
        if user is None:
            raise exceptions.UserNotExists
        return user

    async def get_all_users(
        self,
    ):
        all_users = await self.session.scalars(
            select(self.user_table).options(
                selectinload(self.user_table.founds),
                selectinload(self.user_table.managed_founds),
            )
        )
        return all_users

    async def create_user_with_founds(self, create_dict: Dict[str, Any]):
        founds_ids = create_dict.pop("founds_ids", [])
        user = self.user_table(**create_dict)
        founds_statement = select(models.Found).where(models.Found.id.in_(founds_ids))
        founds = await self.session.scalars(founds_statement)
        for found in founds:
            user.founds.append(found)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def add_nickname_to_user(self, user_id: int, new_nicknames: dict):
        user_statement = select(self.user_table).where(self.user_table.id == user_id)
        user = self.session.scalar(user_statement)
        for room, nickname in new_nicknames.items:
            user.nicknames[room] = nickname
        self.session.commit()
        self.session.refresh(user)
        return user


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[UsersDB, Any]:
    yield UsersDB(session, models.User)
