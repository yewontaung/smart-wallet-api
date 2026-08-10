from sqlmodel import Session

from app.dtos.base import ModificationResult
from app.dtos.manager.inputs import DistrictForm
from app.dtos.shared.outputs import DistrictInfo
from app.dtos.shared.searches import LocationSearch


def search(search:LocationSearch, session:Session) -> list[DistrictInfo]:
    return

def save_district(form:DistrictForm, user_id:int, session:Session) -> ModificationResult:
    return