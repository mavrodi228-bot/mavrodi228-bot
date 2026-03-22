from datetime import date
from app.analytics.engine import AnalyticsEngine
from app.repositories.goal_repository import GoalRepository
from app.repositories.transaction_repository import TransactionRepository
from app.recommendations.engine import RecommendationEngine
from app.schemas.analytics import AnalyticsOverview, CategoryAnalyticsRead, ForecastRead, RecommendationsRead, RecurringPaymentRead
from app.utils.dates import month_bounds, previous_month_bounds


class AnalyticsService:
    def __init__(self, transaction_repository: TransactionRepository, goal_repository: GoalRepository):
        self.transaction_repository = transaction_repository
        self.goal_repository = goal_repository
        self.analytics_engine = AnalyticsEngine()
        self.recommendation_engine = RecommendationEngine(self.analytics_engine)

    def _period_data(self, target_date: date | None = None):
        target_date = target_date or date.today()
        start, end = month_bounds(target_date)
        prev_start, prev_end = previous_month_bounds(target_date)
        transactions = self.transaction_repository.month_transactions(start, end)
        previous = self.transaction_repository.month_transactions(prev_start, prev_end)
        goals = self.goal_repository.list()
        return transactions, previous, goals

    def overview(self, target_date: date | None = None) -> AnalyticsOverview:
        tx, prev, goals = self._period_data(target_date)
        return self.analytics_engine.calculate_overview(tx, prev, goals)

    def categories(self, target_date: date | None = None) -> CategoryAnalyticsRead:
        tx, _, _ = self._period_data(target_date)
        return self.analytics_engine.category_breakdown(tx)

    def recurring(self, target_date: date | None = None) -> list[RecurringPaymentRead]:
        tx, _, _ = self._period_data(target_date)
        return self.analytics_engine.recurring_payments(tx)

    def forecast(self, target_date: date | None = None) -> ForecastRead:
        tx, _, _ = self._period_data(target_date)
        return self.analytics_engine.forecast(tx, target_date)

    def recommendations(self, target_date: date | None = None) -> RecommendationsRead:
        tx, prev, goals = self._period_data(target_date)
        return RecommendationsRead(insights=self.recommendation_engine.build_insights(tx, prev, goals))
