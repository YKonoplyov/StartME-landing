from typing import Any, Optional, Dict

from fastapi import Depends, Request, exceptions
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from fastapi_users.password import PasswordHelper
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import models, exceptions as users_exceptions

import schemas
from utils import exceptions as custom_exceptions 
from auth import BearerTransportRefresh, AuthenticationBackendRefresh
from db.users_db import get_user_db, models as db_models, User, UsersDB

SECRET = "SECRET"
REFRESH_SECRET = "REFRESH_SECRET"

class PasswordHelperV2(PasswordHelper):
    def __init__(self, password_hash: Optional[PasswordHash] = None) -> None:
        if password_hash is None:
            self.password_hash = PasswordHash(
                (
                    BcryptHasher(rounds=10, prefix="2a"),
                )
            )
        else:
            self.password_hash = password_hash  # pragma: no cover
password_helper = PasswordHelperV2()
class UserManager(BaseUserManager[db_models.User, IntegerIDMixin]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    
    
    async def authenticate(
        self, credentials: dict
    ) -> Optional[models.UP]:
        
        try:
            user = await self.user_db.get_by_username_exc(credentials.username)
        except users_exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None
        
        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user
    
    def parse_id(self, value: Any) -> int:
        if isinstance(value, float):
            raise users_exceptions.InvalidID()
        try:
            return int(value)
        except ValueError as e:
            raise users_exceptions.InvalidID() from e

    async def create_with_funds(
        self,
        user_create: schemas.UserCreate,
        # current_user: User,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_username(user_create.username)
        if existing_user is not None:
            raise users_exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        new_user_role = user_dict.get("role")
        # if (
        #     current_user.role == db_models.Roles.READ_ONLY 
        #     and new_user_role != db_models.Roles.READ_ONLY
        # ):
        #     raise custom_exceptions.NotEnoughPermissions()

        # if (
        #     current_user.role == db_models.Roles.USER 
        #     and new_user_role not in [
        #         db_models.Roles.READ_ONLY, db_models.Roles.USER
        #         ]
        # ):
        #     raise custom_exceptions.NotEnoughPermissions()
        
        # if (
        #     current_user.role == db_models.Roles.MANAGER 
        #     and new_user_role == db_models.Roles.ADMIN
        # ):
        #     raise custom_exceptions.NotEnoughPermissions() 
        
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create_user_with_funds(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
    
    async def update(
        self,
        user_update: schemas.UserUpdate,
        user: models.UP,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Update a user.

        Triggers the on_after_update handler on success

        :param user_update: The UserUpdate model containing
        the changes to apply to the user.
        :param user: The current user to update.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the update, defaults to False
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :return: The updated user.
        """
            
        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()
        if user.role in [db_models.Roles.USER, db_models.Roles.READ_ONLY]:
            updated_user.pop("role")
        updated_user = await self._update(user, updated_user_data)
        await self.on_after_update(updated_user, updated_user_data, request)
        return updated_user
    
    async def _update(self, user: models.UP, update_dict: Dict[str, Any]) -> models.UP:
        validated_update_dict = {}
        for field, value in update_dict.items():
            if field == "password" and value is not None:
                await self.validate_password(value, user)
                validated_update_dict["hashed_password"] = self.password_helper.hash(
                    value
                )
            else:
                validated_update_dict[field] = value
        return await self.user_db.update(user, validated_update_dict)
    
    async def get_all_users(self):
        return await self.user_db.get_all_users()

    async def on_after_register(
        self, user: db_models.User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: db_models.User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: db_models.User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: UsersDB = Depends(get_user_db)):
    yield UserManager(user_db, password_helper)


bearer_transport_refresh = BearerTransportRefresh(tokenUrl="auth/jwt/refresh")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=300)

def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=REFRESH_SECRET, lifetime_seconds=259200)

auth_backend = AuthenticationBackendRefresh(
    name="jwt",
    transport=bearer_transport_refresh,
    get_strategy=get_jwt_strategy,
    get_refresh_strategy=get_refresh_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

