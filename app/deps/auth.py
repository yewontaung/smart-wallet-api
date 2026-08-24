from contextvars import ContextVar
from functools import wraps
from http import HTTPStatus
import inspect
from typing import Annotated, Any, Callable, TypeVar, cast

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.data.database import get_session
from app.data.enums import UserType
from app.data.models import ManagerAccount, WalletUserAccount
from app.dtos.base import BaseDto
from app.utils.encryption import decode_jwt
from app.utils.exceptions import SecurityException



class AuthUser(BaseDto):
    user_id:int
    user_name:str # credential
    roles:list[str]
    is_disable:bool = False
    is_deleted:bool = False
    context:dict[str, Any] = {}

__auth_context__ = ContextVar("auth_user", default=None)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

async def require_authentication(token:str = Depends(oauth2_schema), session:Session = Depends(get_session)):
    payload = decode_jwt(token)
    user_type = UserType(payload.get("user_type"))

    match user_type:
        case UserType.WALLET_USER:
            account = session.get(WalletUserAccount, payload.get("account_id"))
        case UserType.MANAGER:
            account = session.get(ManagerAccount, payload.get("account_id"))

    if not account:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid account."
        )

    if isinstance(account, WalletUserAccount):
        auth_user = AuthUser(
            user_id=account.account_id,
            user_name=account.phone_no,
            roles=[account.user_role]
        )
    elif isinstance(account, ManagerAccount):
        auth_user = AuthUser(
            user_id=account.account_id,
            user_name=account.account_email,
            roles=[account.user_type]
        )

    context_token = __auth_context__.set(auth_user)
    try:
        yield
    finally:
        __auth_context__.reset(context_token)

def get_authentication(request:Request) -> AuthUser:
    return cast(AuthUser, __auth_context__.get())

Authentication = Annotated[AuthUser, Depends(get_authentication)]

R = TypeVar("R")

def has_roles(*roles:str):
    allowed = frozenset(roles)

    def decorate(func:Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> R:
            auth_user:AuthUser = __auth_context__.get("auth_user")
            if not auth_user: 
                raise SecurityException("Unauthicated user.")
            if auth_user.is_disable:
                raise SecurityException("Access denied.")
            if auth_user.is_deleted:
                raise SecurityException("User is deleted.")
            if allowed.intersection(frozenset(auth_user.roles)):
                raise SecurityException("Access denied.")

            result = func(*args, **kwargs)
            if inspect.isawaitable(result):
                return await result

            return result

        return wrapper

    return decorate
