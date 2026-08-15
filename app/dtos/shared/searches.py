from sqlmodel import col, or_
from sqlmodel.sql.expression import SelectOfScalar

from datetime import datetime, timezone
from typing import Optional, Type, TypeVar

from app.data.enums import BusinessType
from app.data.models import Account, BusinessApprovalRequest
from app.dtos.base import BaseDto

T = TypeVar("T")

class TransactionSearch(BaseDto):

    q:Optional[str] = None # full name, note, phone no

    operation_id:Optional[int] = None

    amount_from:Optional[float] = None
    amount_to:Optional[float] = None

    date_from:Optional[datetime] = None
    date_to:Optional[datetime] = None

class BusinessProfileSearch(BaseDto):
    q:Optional[str] = None # owner name, qualify name

    business_type:Optional[BusinessType] = None

    created_from:Optional[datetime] = None
    created_to:Optional[datetime] = None

    def where(
            self, 
            query:SelectOfScalar[T], 
            root:Type[BusinessApprovalRequest], 
            join_account:Type[Account]):
        if self.q:
            query = query.where(
                or_(
                    col(root.qualified_name).ilike(f"{self.q}%"),
                    col(join_account.full_name).ilike(f"{self.q}%")
                )
            )

        if self.business_type:
            query = query.where(root.business_type == self.business_type)

        if self.created_from:
            query = query.where(root.created_at >= self.created_from)

        if self.created_to:
            query= query.where(root.created_at <= self.created_to)
        
        return query

class MessageSearch(BaseDto):
    q:Optional[str] = None # user name, phone no, message text

    date_from:Optional[datetime] = None
    date_to:Optional[datetime] = None

class LocationSearch(BaseDto):
    q:Optional[str] = None

    users_from:Optional[int] = None
    users_to:Optional[int] = None

    date_from:Optional[datetime] = None
    date_to:Optional[datetime] = None

class ReceiverSearch(BaseDto):
    phone_no:str