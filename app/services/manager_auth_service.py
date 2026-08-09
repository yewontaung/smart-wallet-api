from sqlmodel import Session

from app.dtos.manager.inputs import ManagerSignInForm
from app.dtos.manager.outputs import ManagerAuthResult


def sign_in(form:ManagerSignInForm, session:Session) -> ManagerAuthResult:
    return