from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import configs
from app.configs import routes
from app.data import database
from app.utils import env


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("====== Starting up Smart Wallet API ======")
    database.create_tables()
    yield
    print("====== Shutting down Smart Wallet API ======")


app = FastAPI(lifespan=lifespan)

app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.annonymous_router)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.manager_router)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.wallet_user_router)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.resource_router)