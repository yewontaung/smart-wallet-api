from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.data import database


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("====== Starting up Smart Wallet API ======")
    database.create_tables()
    yield
    print("====== Shutting down Smart Wallet API ======")


app = FastAPI(lifespan=lifespan)