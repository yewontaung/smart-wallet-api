from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from app.data.base import AuditableModel
from app.data.enums import (
    BusinessApprovalStatus,
    BusinessStatus, 
    BusinessType, 
    ManagerRole, 
    TransactionStatus, 
    TransactionType, 
    UserType, 
    WalletType,
    WalletUserStatus, 
    WalletUserType)
from app.data.meta_models import Township


class NRC(AuditableModel, table=True):
    nrc_id:Optional[int] = Field(primary_key=True, default=None)
    district_code:str = Field(nullable=False)
    township_code:str = Field(nullable=False)
    nrc_type:str = Field(nullable=False)
    nrc_no:str = Field(nullable=False)

    user_id:int = Field(foreign_key="user.user_id")
    user:Optional["User"] = Relationship(back_populates="nrc")

class Address(AuditableModel, table=True):
    address_id:Optional[int] = Field(primary_key=True, default=None)
    address_content:str = Field(nullable=False)

    township_id:int = Field(foreign_key="township.township_id")
    township:Optional[Township] = Relationship()

    user_id:int = Field(foreign_key="user.user_id")
    user:Optional["User"] = Relationship(back_populates="address")

class User(AuditableModel, table=True):
    user_id:Optional[int] = Field(primary_key=True, default=None)
    full_name:str = Field(nullable=False)    

    user_type:UserType = Field(nullable=False)
    profile_url:Optional[str] = Field(nullable=True)

    is_disable:bool = Field(default=False)
    is_deleted:bool = Field(default=False)

    nrc_id:int = Field(foreign_key="nrc.nrc_id")
    nrc:Optional[NRC] = Relationship(back_populates="user")

    address_id:int = Field(foreign_key="address.address_id")
    address:Optional[Address] = Relationship(back_populates="user")


class WalletUserAccount(AuditableModel, table=True):
    user_id:int = Field(primary_key=True, foreign_key="user.user_id", nullable=False)
    phone_no:str = Field(nullable=False, unique=True, index=True)
    pin:str = Field(nullable=False)

    nick_name:Optional[str] = Field(nullable=True)

    hashed_password:Optional[str] = Field(nullable=True)
    account_type:WalletUserType = Field(nullable=False, default=WalletUserType.NORMAL)

    account_status:WalletUserStatus = Field(nullable=False, default=WalletUserStatus.PENDING)

    user:Optional[User] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[WalletUserAccount.user_id]"
    })

    approved_by:Optional[int] = Field(nullable=True, foreign_key="user.user_id")
    approver:Optional[User] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[WalletUserAccount.approved_by]"
    })

    wallets:list["Wallet"] = Relationship(back_populates="wallet_user")
    support_chat:Optional["CustomerSupportChat"] = Relationship(back_populates="wallet_user")


class ManagerAccount(AuditableModel, table=True):
    user_id:int = Field(primary_key=True, foreign_key="user.user_id", nullable=False)
    phone_no:str = Field(nullable=False, unique=True, index=True)
    account_email:str = Field(nullable=False, unique=True, index=True)
    hashed_password:str = Field(nullable=False)
    role:ManagerRole = Field(nullable=False)

    user:Optional[User] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[User.user_id]"
    })


class Wallet(AuditableModel, table=True):
    wallet_id:Optional[int] = Field(primary_key=True, default=None)
    wallet_type:WalletType = Field(nullable=False, default=WalletType.FUNDING)
    current_balance:float = Field(nullable=False, ge=0)
    last_balance:float = Field(nullable=False, ge=0)
    version:int = Field(nullable=False, ge=0, default=0)

    wallet_user_id:int = Field(foreign_key="walletuseraccount.user_id")
    wallet_user:Optional[WalletUserAccount] = Relationship(back_populates="wallets", sa_relationship_kwargs={
        "foreign_keys": "[Wallet.wallet_user_id]"
    })

    approved_by:Optional[int] = Field(nullable=True, foreign_key="manageraccount.user_id")
    approver:Optional[ManagerAccount] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[Wallet.approved_by]"
    })

class WalletOperation(AuditableModel, table=True):
    operation_id:Optional[int] = Field(primary_key=True, default=None)
    operation_name:str = Field(nullable=False, unique=True, index=True)

    transactions:list["Transaction"] = Relationship(back_populates="operation")

class Transaction(AuditableModel, table=True):
    trx_id:Optional[UUID] = Field(primary_key=True, default=uuid4)
    amount:float = Field(nullable=False, gt=0)
    status:TransactionStatus = Field(nullable=False)
    note:Optional[str] = Field(nullable=True)

    operation_id:int = Field(foreign_key="walletoperation.operation_id")
    operation:Optional[WalletOperation] = Relationship(back_populates="transactions")

    receiver_wallet_id:int = Field(foreign_key="wallet.wallet_id")
    receiver_wallet:Optional[Wallet] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[Transaction.receiver_wallet_id]"
    })

    sender_wallet_id:int = Field(foreign_key="wallet.wallet_id")
    sender_wallet:Optional[Wallet] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[Transaction.sender_wallet_id]"
    })


class TransactionLog(AuditableModel, table=True):
    log_id:Optional[UUID] = Field(primary_key=True, default=uuid4)
    trx_type:TransactionType = Field(nullable=False)

    wallet_id:int = Field(foreign_key="wallet.wallet_id")
    wallet:Optional[Wallet] = Relationship()

    trx_id:UUID = Field(foreign_key="transaction.trx_id")
    transaction:Optional[Transaction] = Relationship()

class BusinessApprovalRequest(AuditableModel, table=True):
    request_id:Optional[int] = Field(primary_key=True, default=None)
    qualified_name:str = Field(nullable=False)
    description:str = Field(nullable=False)
    banner_url:Optional[str] = Field(nullable=True)
    business_type:BusinessType = Field(nullable=False)
    status:BusinessApprovalStatus = Field(nullable=False, default=BusinessApprovalStatus.PENDING)
    remark:Optional[str] = Field(nullable=True)

    owner_id:int = Field(foreign_key="walletuseraccount.user_id")
    owner:Optional[WalletUserAccount] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[BusinessApprovalRequest.owner_id]"
    })

    updated_by:Optional[int] = Field(nullable=True, foreign_key="manageraccount.user_id")
    updator:Optional[ManagerAccount] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[BusinessApprovalRequest.updated_by]"
    })

    
class BusinessProfile(AuditableModel, table=True):
    business_id:Optional[int] = Field(primary_key=True, default=None)
    qualified_name:str = Field(nullable=False, unique=True)
    description:str = Field(nullable=False)
    banner_url:Optional[str] = Field(nullable=True)
    business_type:BusinessType = Field(nullable=False)
    is_deleted:bool = Field(nullable=False, default=False)
    status:BusinessStatus = Field(nullable=False, default=BusinessStatus.OPEN)

    owner_id:int = Field(foreign_key="walletuseraccount.user_id")
    owner:Optional[WalletUserAccount] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[BusinessProfile.owner_id]"
    })

    approved_by:Optional[int] = Field(nullable=True, foreign_key="manageraccount.user_id")
    approver:Optional[ManagerAccount] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[BusinessProfile.approved_by]"
    })

class CustomerSupportChat(AuditableModel, table=True):
    chat_id:int = Field(primary_key=True, foreign_key="walletuseraccount.user_id", ondelete="CASCADE")
    wallet_user:Optional[WalletUserAccount] = Relationship(back_populates="support_chat")

    messages:list["ChatMessage"] = Relationship(back_populates="support_chat")

class ChatMessage(AuditableModel, table=True):
    message_id:Optional[int] = Field(primary_key=True, default=None)
    message_content:str = Field(nullable=False)
    is_read:bool = Field(default=False)

    user_id:int = Field(foreign_key="user.user_id")
    user:Optional[User] = Relationship()

    support_chat_id:int = Field(foreign_key="customersupportchat.chat_id", ondelete="CASCADE")
    support_chat:Optional[CustomerSupportChat] = Relationship(back_populates="messages")
