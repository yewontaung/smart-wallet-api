from sqlmodel import Session

from app.dtos.manager.inputs import ManagerForm
from app.dtos.manager.searches import ManagerSearch


def search(search:ManagerSearch, page:int, size:int, session:Session):
    return

def add_manager(form:ManagerForm, user_id:int, session:Session):
    return