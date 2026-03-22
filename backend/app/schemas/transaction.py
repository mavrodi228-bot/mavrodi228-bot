from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.category import CategoryRead
from app.schemas.common import ORMModel


class TransactionRead(ORMModel):
    id: int
    external_id: str | None
    source_type: str
    account_id: str | None
    date: date
    posted_at: datetime | None
    amount: Decimal
    currency: str
    direction: str
    description: str
    merchant: str | None
    mcc: str | None
    category_id: int | None
    raw_category: str | None
    is_recurring: bool
    is_transfer: bool
    is_hidden: bool
    category: CategoryRead | None = None


class TransactionUpdateCategory(BaseModel):
    category_id: int | None = Field(default=None)
