from sqlmodel import SQLModel, Session, create_engine

from app.utils import env
from app.data.models import *


engine = create_engine(url=env.DATABASE_URL, echo=env.SHOW_SQL)

def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    SQLModel.metadata.create_all(engine)