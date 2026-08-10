from sqlmodel import Session

from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.inputs import TownshipForm
from app.dtos.shared.outputs import TownshipInfo
from app.dtos.shared.searches import LocationSearch


def search(search:LocationSearch, page:int, size:int, session:Session) -> PageResult[TownshipInfo]:
    return

def save_district(form:TownshipForm, user_id:int, session:Session) -> ModificationResult:
    return