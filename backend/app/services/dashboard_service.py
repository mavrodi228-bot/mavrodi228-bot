from datetime import date
from app.analytics.engine import AnalyticsEngine
from app.repositories.goal_repository import GoalRepository
from app.repositories.transaction_repository import TransactionRepository
from app.recommendations.engine import RecommendationEngine
from app.schemas.dashboard import DashboardSummary, FinancialStabilityScore
from app.schemas.common import ChartPoint, MoneyPoint
from app.utils.dates import month_bounds, previous_month_bounds


class DashboardService:
    def __init__(self, transaction_repository: TransactionRepository, goal_repository: GoalRepository):
        self.transaction_repository = transaction_repository
        self.goal_repository = goal_repository
        self.analytics_engine = AnalyticsEngine()
        self.recommendation_engine = RecommendationEngine(self.analytics_engine)

    def summary(self, target_date: date | None = None) -> DashboardSummary:
        target_date = target_date or date.today()
        start, end = month_bounds(target_date)
        prev_start, prev_end = previous_month_bounds(target_date)
        transactions = self.transaction_repository.month_transactions(start, end)
        previous_transactions = self.transaction_repository.month_transactions(prev_start, prev_end)
        goals = self.goal_repository.list()
        category_data = self.analytics_engine.category_breakdown(transactions)
        forecast = self.analytics_engine.forecast(transactions, target_date)
        overview = self.analytics_engine.calculate_overview(transactions, previous_transactions, goals)
        score = self.analytics_engine.financial_stability_score(transactions, goals)
        insights = self.recommendation_engine.build_insights(transactions, previous_transactions, goals)
        return DashboardSummary(
            total_income=overview.total_income,
            total_expenses=overview.total_expenses,
            net_balance=overview.net_balance,
            forecast_expenses=forecast.forecast_expenses,
            forecast_balance=forecast.forecast_balance,
            top_expense_categories=category_data.top_categories,
            daily_spend_chart=category_data.spend_timeline,
            category_share_chart=category_data.category_shares,
            insights=insights,
            stability_score=FinancialStabilityScore(**score),
        )
