from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DateRangeParams(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


class MoneyPoint(BaseModel):
    label: str
    amount: Decimal


class ChartPoint(BaseModel):
    date: date | str
    value: Decimal | float


class Insight(BaseModel):
    title: str
    description: str
    severity: str = 'info'


class ImportResult(BaseModel):
    imported_rows: int
    skipped_rows: int
    errors: list[str] = []


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
