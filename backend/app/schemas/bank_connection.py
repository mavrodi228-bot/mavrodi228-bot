from datetime import datetime
from pydantic import BaseModel
from app.schemas.common import ORMModel


class BankConnectionCreate(BaseModel):
    provider_name: str
    is_active: bool = True
    auth_type: str
    credentials: dict[str, str]


class BankConnectionRead(ORMModel):
    id: int
    provider_name: str
    is_active: bool
    auth_type: str
    created_at: datetime
    updated_at: datetime
