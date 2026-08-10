from sqlmodel import Session

from app.dtos.action.inputs import MobileTopUpForm, PayBillForm, SendMoneyForm
from app.dtos.action.outputs import ActionResult


def send_money(form:SendMoneyForm, user_id:int, session:Session) -> ActionResult:
    return

def pay_bill(form:PayBillForm, user_id:int, session:Session) -> ActionResult:
    return

def top_up(form:MobileTopUpForm, auth_user:int, session:Session) -> ActionResult:
    return