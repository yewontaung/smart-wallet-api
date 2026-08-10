from sqlmodel import Session

from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.inputs import ManagerForm
from app.dtos.manager.outputs import ManagerListItem
from app.dtos.manager.searches import ManagerSearch


def search(search:ManagerSearch, page:int, size:int, session:Session) -> PageResult[ManagerListItem]:
    return

def add_manager(form:ManagerForm, user_id:int, session:Session) -> ModificationResult[int]:
    return