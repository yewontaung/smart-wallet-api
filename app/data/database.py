from typing import TypeVar

from sqlmodel import SQLModel, Session, create_engine

from app.utils import env
from app.data.models import *
from app.utils.exceptions import ResourceNotFoundException


engine = create_engine(url=env.DATABASE_URL, echo=env.SHOW_SQL)

def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    SQLModel.metadata.create_all(engine)

T = TypeVar("T")
def safe_call(t:T | None, model:str, key:str, value:str) -> T:
    if not t:
        raise ResourceNotFoundException(f"{model} with {key}: {value} is not found.")
    return t