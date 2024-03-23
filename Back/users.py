from typing import Any, Optional

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
from db.users_db import get_user_db, models as db_models, User, UsersDB

SECRET = "SECRET"


# class PasswordHelper(PasswordHelperProtocol):
#     def __init__(self, password_hash: Optional[PasswordHash] = None) -> None:
#         if password_hash is None:
#             self.password_hash = PasswordHash(
#                 (
#                     Argon2Hasher(),
#                     BcryptHasher(),
#                 )
#             )
#         else:
#             self.password_hash = password_hash  # pragma: no cover

#     def verify_and_update(
#         self, plain_password: str, hashed_password: str
#     ) -> Tuple[bool, Union[str, None]]:
#         return self.password_hash.verify_and_update(plain_password, hashed_password)

#     def hash(self, password: str) -> str:
#         return self.password_hash.hash(password)

#     def generate(self) -> str:
#         return secrets.token_urlsafe()

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

class UserManager(BaseUserManager[db_models.User, IntegerIDMixin]):
    password_helper = PasswordHelperV2()
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    async def authenticate(
        self, credentials: dict
    ) -> Optional[models.UP]:
        
        try:
            user = await self.user_db.get_by_username(credentials.username)
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

    async def create_with_founds(
        self,
        user_create: schemas.UserCreate,
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

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create_user_with_founds(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

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
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[db_models.User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
