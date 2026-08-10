from sqlmodel import Session

from app.dtos.base import ModificationResult, PageResult
from app.dtos.shared.outputs import BusinessProfileListItem, ProviderProfile
from app.dtos.shared.searches import BusinessProfileSearch
from app.dtos.wallet_user.inputs import BusinessProfileForm


def search(search:BusinessProfileSearch, page:int, size:int, session:Session) -> PageResult[BusinessProfileListItem]:
    return

def search_provider_by_id(provider_id:int, session:Session) -> ProviderProfile:
    return

def search_by_owner_id(search:BusinessProfileSearch, user_id:int, page:int, size:int, session:Session) -> PageResult[BusinessProfileListItem]:
    return

def apply_request(form:BusinessProfileForm, user_id:int, session:Session) -> ModificationResult:
    return