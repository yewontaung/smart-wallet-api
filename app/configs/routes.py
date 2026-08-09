from fastapi import APIRouter

from app.api.manager import (
    account_api, 
    auth_api as manager_auth_api,
    business_api as manager_business_api,
    manager_api, 
    me_api as manager_me_api,
    support_chat_api as manager_support_chat_api,
    transaction_api)
from app.api.wallet_user import (
    action_api,
    ai_api,
    auth_api,
    business_api,
    me_api,
    support_chat_api,)


annonymous_router = APIRouter()
manager_router = APIRouter(prefix="/manager")
wallet_user_router = APIRouter(prefix="/wallet-user")

# annonymous routes registration
annonymous_router.include_router(prefix="/manager", router=manager_auth_api.router)
annonymous_router.include_router(prefix="/wallet-user", router=auth_api.router)


# Manager routes registration
manager_router.include_router(router=account_api.router)
manager_router.include_router(router=manager_me_api.router)
manager_router.include_router(router=transaction_api.router)
manager_router.include_router(router=manager_api.router)
manager_router.include_router(router=manager_business_api.router)
manager_router.include_router(router=manager_support_chat_api.router)

# Wallet user routes registration
wallet_user_router.include_router(router=me_api.router)
wallet_user_router.include_router(router=support_chat_api.router)
wallet_user_router.include_router(router=action_api.router)
wallet_user_router.include_router(router=ai_api.router)
wallet_user_router.include_router(router=business_api.router)


