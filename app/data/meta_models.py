from typing import Optional

from sqlmodel import Field, Relationship

from app.data.base import AuditableModel


class District(AuditableModel, table=True):
    district_id:Optional[int] = Field(primary_key=True, default=None)
    district_name:str = Field(nullable=False, unique=True, index=True)
    townships:list["Township"] = Relationship(back_populates="district")

class Township(AuditableModel, table=True):
    township_id:Optional[int] = Field(primary_key=True, default=None)
    township_name:str = Field(nullable=False, unique=True, index=True)

    district_id:int = Field(nullable=False, foreign_key="district.district_id")
    district:Optional[District] = Relationship(back_populates="townships")