from decimal import Decimal
from pydantic import BaseModel
from app.schemas.common import ChartPoint, Insight, MoneyPoint


class AnalyticsOverview(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal
    average_daily_spending: Decimal
    average_transaction_amount: Decimal
    month_over_month_delta: Decimal
    weekend_vs_weekday_ratio: float
    small_frequent_expenses_total: Decimal
    financial_stability_score: int


class RecurringPaymentRead(BaseModel):
    merchant: str
    average_amount: Decimal
    occurrences: int
    next_expected_date: str


class ForecastRead(BaseModel):
    forecast_expenses: Decimal
    forecast_balance: Decimal
    recurring_projection: Decimal
    pace_projection: Decimal


class CategoryAnalyticsRead(BaseModel):
    top_categories: list[MoneyPoint]
    category_shares: list[MoneyPoint]
    spend_timeline: list[ChartPoint]


class RecommendationsRead(BaseModel):
    insights: list[Insight]
