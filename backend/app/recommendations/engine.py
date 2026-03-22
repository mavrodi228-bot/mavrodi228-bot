from decimal import Decimal
from app.analytics.engine import AnalyticsEngine
from app.models.goal import Goal
from app.models.transaction import Transaction
from app.schemas.common import Insight


class RecommendationEngine:
    def __init__(self, analytics_engine: AnalyticsEngine):
        self.analytics_engine = analytics_engine

    def build_insights(self, transactions: list[Transaction], previous_transactions: list[Transaction], goals: list[Goal]) -> list[Insight]:
        category_data = self.analytics_engine.category_breakdown(transactions)
        forecast = self.analytics_engine.forecast(transactions)
        recurring = self.analytics_engine.recurring_payments(transactions)
        overview = self.analytics_engine.calculate_overview(transactions, previous_transactions, goals)
        insights: list[Insight] = []
        if category_data.top_categories:
            top = category_data.top_categories[0]
            insights.append(Insight(title='Top expense category', description=f'{top.label} leads this month with {top.amount} RUB.'))
        if overview.month_over_month_delta:
            direction = 'up' if overview.month_over_month_delta > 0 else 'down'
            insights.append(Insight(title='Month-over-month change', description=f'Expenses are {direction} by {abs(overview.month_over_month_delta)} RUB versus last month.'))
        if recurring:
            recurring_total = sum((item.average_amount for item in recurring), Decimal('0')).quantize(Decimal('0.01'))
            insights.append(Insight(title='Recurring burden', description=f'Recurring payments track at ~{recurring_total} RUB monthly.', severity='warning'))
        if overview.weekend_vs_weekday_ratio > 1.1:
            insights.append(Insight(title='Weekend spending', description='Weekend spending is materially higher than weekdays.', severity='warning'))
        insights.append(Insight(title='Forecast', description=f'Projected month-end balance is {forecast.forecast_balance} RUB.'))
        if goals:
            stalled = [goal for goal in goals if goal.status == 'active' and goal.current_amount < goal.target_amount * Decimal('0.25')]
            if stalled:
                insights.append(Insight(title='Goal acceleration', description='Redirect part of your free cash flow into underfunded goals.'))
        return insights[:6]
