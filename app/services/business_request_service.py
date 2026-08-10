from sqlmodel import Session

from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.inputs import BusinessRequestRejectForm, BusinessRequestStatusChangeForm
from app.dtos.manager.outputs import BusinessRequestListItem
from app.dtos.shared.searches import BusinessProfileSearch


def search(search:BusinessProfileSearch, page:int, size:int, session:Session) -> PageResult[BusinessRequestListItem]:
    return

def approve(request_id:int, manager_id:int, session:Session) -> ModificationResult:
    return

def reject(form:BusinessRequestRejectForm, request_id:int, manager_id:int, session:Session) -> ModificationResult:
    return

def change_status(form:BusinessRequestStatusChangeForm, request_id:int, manager_id:int, session:Session) -> ModificationResult:
    return