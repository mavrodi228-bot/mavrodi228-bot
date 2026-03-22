from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from app.schemas.common import ORMModel


class GoalCreate(BaseModel):
    title: str
    target_amount: Decimal
    current_amount: Decimal = 0
    deadline: date | None = None
    monthly_target: Decimal | None = None
    status: str = 'active'


class GoalUpdate(BaseModel):
    title: str | None = None
    target_amount: Decimal | None = None
    current_amount: Decimal | None = None
    deadline: date | None = None
    monthly_target: Decimal | None = None
    status: str | None = None


class GoalRead(ORMModel):
    id: int
    title: str
    target_amount: Decimal
    current_amount: Decimal
    deadline: date | None
    monthly_target: Decimal | None
    status: str
    created_at: datetime
    updated_at: datetime
    progress_percent: float = 0
    estimated_completion_date: date | None = None
