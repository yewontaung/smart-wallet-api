from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import configs
from app.configs import routes
from app.data import database
from app.handlers.exception_handlers import (
    handle_business_exception,
    handle_resource_not_found_exception,
    handle_unauthorized_wallet_exception,
    handle_insufficient_balance_exception
)
from app.utils import env
from app.utils.exceptions import (
    BusinessException, 
    ResourceNotFoundException, 
    UnauthorizedWalletException, 
    InsufficientBalanceException
)


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("====== Starting up Smart Wallet API ======")
    database.create_tables()
    yield
    print("====== Shutting down Smart Wallet API ======")


app = FastAPI(lifespan=lifespan)

origins = env.ALLOW_ORIGINS.split(",")

"""
CORS configs
"""
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=origins,
)

"""
Endpoints registration
"""
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.annonymous_router)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.manager_router)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.wallet_user_router)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.resource_router)

"""
Exception handlers registration
"""
app.add_exception_handler(BusinessException, handle_business_exception)
app.add_exception_handler(ResourceNotFoundException, handle_resource_not_found_exception)
app.add_exception_handler(UnauthorizedWalletException, handle_unauthorized_wallet_exception)
app.add_exception_handler(InsufficientBalanceException, handle_insufficient_balance_exception)