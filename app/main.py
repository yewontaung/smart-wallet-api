from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import configs
from app.configs import routes
from app.data import database
from app.handlers.exception_handlers import handle_resource_not_found_exception
from app.utils import env
from app.utils.exceptions import ResourceNotFoundException


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("====== Starting up Smart Wallet API ======")
    database.create_tables()
    yield
    print("====== Shutting down Smart Wallet API ======")


app = FastAPI(lifespan=lifespan)


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
app.add_exception_handler(ResourceNotFoundException, handle_resource_not_found_exception)