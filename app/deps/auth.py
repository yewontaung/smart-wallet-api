from typing import Annotated, Any

from fastapi import Depends, Request

from app.dtos.base import BaseDto


class AuthUser(BaseDto):
    user_id:int
    user_name:str # credential
    roles:list[str]
    is_disable:bool = False
    is_deleted:bool = False
    context:dict[str, Any] = {}

def require_manager_authentication():
    ...

def manager_authentication(request:Request) -> AuthUser:
    return AuthUser(
        user_id=1,
        user_name="aung@gmil.com",
        roles=["Admin"],
    )

ManagerAuthentication = Annotated[AuthUser, Depends(manager_authentication)]

def require_wallet_user_authentication():
    ...

def wallet_user_authentication(request:Request) -> AuthUser:
    return AuthUser(
        user_id=4,
        user_name="user@gmil.com",
        roles=["user"],
    )

WalletUserAuthentication = Annotated[AuthUser, Depends(wallet_user_authentication)]
