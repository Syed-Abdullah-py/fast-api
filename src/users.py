import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users.db import (
    SQLAlchemyUserDatabase,
)
from src.db import User, get_user_db
from src.schemas import UserCreate

load_dotenv()

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = os.getenv("SECRET")
    verification_token_secret = os.getenv("SECRET")

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None
    ) -> None:
        print(f"User has been registered: {user.id}. Verification token: {self.verification_token_secret}")

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None
    ):
        print(f"User {user.id} has been forgot password")


    async def on_after_request(
            self,
            user: User,
            request: Optional[Request] = None
    ):
        print(f"Verification request has been submitted for user: {user.id}. Verification token: {self.verification_token_secret}")


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=os.getenv("SECRET"), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

