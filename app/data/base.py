from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AuditableModel(SQLModel):
    created_at:datetime = Field(default=lambda:datetime.now(tz=timezone.utc))
    updated_at:datetime = Field(default=lambda:datetime.now(tz=timezone.utc))
