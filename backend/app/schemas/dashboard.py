from decimal import Decimal
from app.schemas.common import ChartPoint, Insight, MoneyPoint
from pydantic import BaseModel


class FinancialStabilityScore(BaseModel):
    score: int
    summary: str
    drivers: list[str]
    improvements: list[str]


class DashboardSummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal
    forecast_expenses: Decimal
    forecast_balance: Decimal
    top_expense_categories: list[MoneyPoint]
    daily_spend_chart: list[ChartPoint]
    category_share_chart: list[MoneyPoint]
    insights: list[Insight]
    stability_score: FinancialStabilityScore
