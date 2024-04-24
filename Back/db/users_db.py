from typing import Any, AsyncGenerator, Dict

from fastapi import Depends
from sqlalchemy import select, func
from fastapi_users import exceptions
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

import models
from models import User
from db.engine import get_async_session


class UsersDB(SQLAlchemyUserDatabase):
    async def get(self, user_id: int) -> User:
        user_statement = (
            select(User).where(User.id == user_id).options(selectinload(User.funds))
        )
        user = await self.session.scalar(user_statement)

        return user

    async def update(self, user: User, update_dict: Dict[str, Any]) -> User:
        fund_ids = update_dict.get("foudns_ids")

        if fund_ids:
            funds_statement = select(models.Fund).where(models.Fund.id.in_(fund_ids))
            funds = self.session.scalars(funds_statement)

            for fund in funds:
                user.funds.append(fund)

        for key, value in update_dict.items():
            setattr(user, key, value)

        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_by_username_exc(self, username: str):
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        user = await self._get_user(statement)

        if user is None:
            raise exceptions.UserNotExists

        return user

    async def get_by_username(self, username: str):
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        user = await self._get_user(statement)

        if user is None:
            return user

    async def get_all_users(self):
        all_users = await self.session.scalars(
            select(self.user_table).options(
                selectinload(self.user_table.funds),
                selectinload(self.user_table.managed_funds),
            )
        )
        return all_users

    async def create_user_with_funds(self, create_dict: Dict[str, Any]):
        funds_ids = create_dict.pop("funds_ids", [])
        user = self.user_table(**create_dict)
        funds_statement = select(models.Fund).where(models.Fund.id.in_(funds_ids))
        funds = await self.session.scalars(funds_statement)

        for fund in funds:
            user.funds.append(fund)

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
