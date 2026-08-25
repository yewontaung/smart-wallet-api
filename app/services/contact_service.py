from sqlmodel import Session, select

from app.data.database import safe_call
from app.data.models import Contact, WalletUserAccount
from app.dtos.base import ModificationResult
from app.dtos.wallet_user.inputs import ContactForm
from app.dtos.wallet_user.outputs import ContactListItem
from app.utils.exceptions import BusinessException


def search(account_id:int, session:Session) -> list[ContactListItem]:
    wallet_user = safe_call(session.get(WalletUserAccount, account_id), "WalletUserAccount", "account_id", account_id)
    return [ContactListItem(
        contact_id=item.contact_id,
        owner_id=item.owner_id,
        contact_name=item.contact_name,
        contact_phone=item.contact_phone,
        has_account=item.has_account,
    ) for item in wallet_user.contacts]

def create(form:ContactForm, account_id:int, session:Session) -> ModificationResult:
    wallet_user = safe_call(session.get(WalletUserAccount, account_id), "WalletUserAccount", "account_id", account_id)
    existed = session.exec(
        select(Contact).where(Contact.owner_id == wallet_user.account_id, Contact.contact_phone == form.phone)
    ).first()

    if existed:
        raise BusinessException(f"Contact with phone {form.phone} has already existed.")

    has_account = session.exec(
        select(WalletUserAccount).where(WalletUserAccount.phone_no == form.phone)
    ).first()

    contact = Contact(
        contact_name=form.name,
        contact_phone=form.phone,
        has_account=True if has_account else False,
        owner_id=wallet_user.account_id,
    )

    session.add(contact)
    session.commit()
    session.refresh(contact)

    return ModificationResult(
        result_item=ContactListItem(
            contact_id=contact.contact_id,
            contact_phone=contact.contact_phone,
            has_account=contact.has_account,
            contact_name=contact.contact_name,
            owner_id=contact.owner_id,
        ),
        is_success=True,
        message=f"Contact with phone {form.phone} is successfully created."
    )
    
def remove(contact_id:int, account_id:int, session:Session) -> ModificationResult:
    contact = safe_call(session.get(Contact, contact_id), "Contact", "contact_id", contact_id)

    if contact.owner_id != account_id:
        raise BusinessException("Access Denied to delete the contact.")

    session.delete(contact)
    session.commit()

    return ModificationResult(
        result_item=contact_id,
        is_success=True,
        message="Contact is deleted successfully."
    )