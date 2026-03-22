from app.analytics.engine import AnalyticsEngine


def test_analytics_overview(sample_transactions, previous_transactions, goals):
    engine = AnalyticsEngine()
    overview = engine.calculate_overview(sample_transactions, previous_transactions, goals)
    assert overview.total_income > overview.total_expenses
    assert overview.financial_stability_score >= 0


def test_recurring_detection(sample_transactions):
    engine = AnalyticsEngine()
    recurring = engine.recurring_payments(sample_transactions)
    assert any(item.merchant == 'Netflix' for item in recurring)
