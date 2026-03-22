from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from statistics import pstdev
from app.models.goal import Goal
from app.models.transaction import Transaction
from app.schemas.analytics import AnalyticsOverview, CategoryAnalyticsRead, ForecastRead, RecurringPaymentRead
from app.schemas.common import ChartPoint, MoneyPoint


@dataclass
class RecurringCluster:
    merchant: str
    amounts: list[Decimal]
    dates: list[date]


class AnalyticsEngine:
    def calculate_overview(self, transactions: list[Transaction], previous_transactions: list[Transaction], goals: list[Goal]) -> AnalyticsOverview:
        income = self._sum_direction(transactions, 'income')
        expenses = self._sum_direction(transactions, 'expense')
        net_balance = income - expenses
        daily_spend = self._daily_spend(transactions)
        average_daily = (sum(daily_spend.values(), Decimal('0')) / max(len(daily_spend), 1)).quantize(Decimal('0.01'))
        average_tx = (sum((tx.amount for tx in transactions), Decimal('0')) / max(len(transactions), 1)).quantize(Decimal('0.01'))
        prev_expenses = self._sum_direction(previous_transactions, 'expense')
        delta = (expenses - prev_expenses).quantize(Decimal('0.01'))
        weekend = sum((tx.amount for tx in transactions if tx.direction == 'expense' and tx.date.weekday() >= 5), Decimal('0'))
        weekday = sum((tx.amount for tx in transactions if tx.direction == 'expense' and tx.date.weekday() < 5), Decimal('0'))
        ratio = float(weekend / weekday) if weekday else 0.0
        small_frequent = sum((tx.amount for tx in transactions if tx.direction == 'expense' and tx.amount <= Decimal('500')), Decimal('0'))
        score = self.financial_stability_score(transactions, goals)['score']
        return AnalyticsOverview(
            total_income=income,
            total_expenses=expenses,
            net_balance=net_balance,
            average_daily_spending=average_daily,
            average_transaction_amount=average_tx,
            month_over_month_delta=delta,
            weekend_vs_weekday_ratio=ratio,
            small_frequent_expenses_total=small_frequent,
            financial_stability_score=score,
        )

    def category_breakdown(self, transactions: list[Transaction]) -> CategoryAnalyticsRead:
        category_totals: dict[str, Decimal] = defaultdict(lambda: Decimal('0'))
        timeline: dict[date, Decimal] = defaultdict(lambda: Decimal('0'))
        for tx in transactions:
            if tx.direction != 'expense':
                continue
            name = tx.category.name if tx.category else 'Other'
            category_totals[name] += tx.amount
            timeline[tx.date] += tx.amount
        top = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)[:8]
        total_expenses = sum(category_totals.values(), Decimal('0')) or Decimal('1')
        shares = [MoneyPoint(label=name, amount=((amount / total_expenses) * Decimal('100')).quantize(Decimal('0.01'))) for name, amount in top]
        return CategoryAnalyticsRead(
            top_categories=[MoneyPoint(label=name, amount=amount) for name, amount in top],
            category_shares=shares,
            spend_timeline=[ChartPoint(date=day, value=amount) for day, amount in sorted(timeline.items())],
        )

    def recurring_payments(self, transactions: list[Transaction]) -> list[RecurringPaymentRead]:
        buckets: dict[str, RecurringCluster] = {}
        for tx in transactions:
            if tx.direction != 'expense' or not tx.merchant:
                continue
            merchant = tx.merchant.lower()
            cluster = buckets.setdefault(merchant, RecurringCluster(merchant=tx.merchant, amounts=[], dates=[]))
            cluster.amounts.append(tx.amount)
            cluster.dates.append(tx.date)
        recurring = []
        for cluster in buckets.values():
            if len(cluster.dates) < 2:
                continue
            date_gaps = sorted((b - a).days for a, b in zip(sorted(cluster.dates), sorted(cluster.dates)[1:]))
            if not date_gaps:
                continue
            avg_gap = sum(date_gaps) / len(date_gaps)
            if avg_gap <= 40:
                next_expected = max(cluster.dates) + timedelta(days=round(avg_gap))
                recurring.append(
                    RecurringPaymentRead(
                        merchant=cluster.merchant,
                        average_amount=(sum(cluster.amounts, Decimal('0')) / len(cluster.amounts)).quantize(Decimal('0.01')),
                        occurrences=len(cluster.amounts),
                        next_expected_date=next_expected.isoformat(),
                    )
                )
        return sorted(recurring, key=lambda item: item.average_amount, reverse=True)

    def forecast(self, transactions: list[Transaction], today: date | None = None) -> ForecastRead:
        today = today or date.today()
        month_start = today.replace(day=1)
        days_passed = max((today - month_start).days + 1, 1)
        month_days = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        expenses = self._sum_direction(transactions, 'expense')
        income = self._sum_direction(transactions, 'income')
        pace_projection = (expenses / days_passed * month_days.day).quantize(Decimal('0.01')) if expenses else Decimal('0.00')
        recurring_projection = sum((item.average_amount for item in self.recurring_payments(transactions)), Decimal('0'))
        forecast_expenses = max(pace_projection, expenses + recurring_projection).quantize(Decimal('0.01'))
        forecast_balance = (income - forecast_expenses).quantize(Decimal('0.01'))
        return ForecastRead(
            forecast_expenses=forecast_expenses,
            forecast_balance=forecast_balance,
            recurring_projection=recurring_projection.quantize(Decimal('0.01')),
            pace_projection=pace_projection,
        )

    def financial_stability_score(self, transactions: list[Transaction], goals: list[Goal]) -> dict:
        income = self._sum_direction(transactions, 'income') or Decimal('1')
        expenses = self._sum_direction(transactions, 'expense')
        net = income - expenses
        recurring_total = sum((item.average_amount for item in self.recurring_payments(transactions)), Decimal('0'))
        essential_slugs = {'housing', 'groceries', 'transport', 'pharmacy', 'subscriptions'}
        essential = sum(
            (tx.amount for tx in transactions if tx.direction == 'expense' and tx.category and tx.category.slug in essential_slugs),
            Decimal('0'),
        )
        free_cash_ratio = max((net / income), Decimal('0'))
        essential_ratio = essential / income
        recurring_ratio = recurring_total / income if income else Decimal('0')
        expense_series = [float(tx.amount) for tx in transactions if tx.direction == 'expense']
        volatility = pstdev(expense_series) if len(expense_series) > 1 else 0
        goal_progress = 0.0
        if goals:
            progress_values = [float((goal.current_amount / goal.target_amount) * 100) for goal in goals if goal.target_amount]
            goal_progress = sum(progress_values) / max(len(progress_values), 1)
        score = 50
        if net > 0:
            score += 15
        score += max(min(int(float(free_cash_ratio) * 25), 20), 0)
        score -= min(int(float(essential_ratio) * 20), 15)
        score -= min(int(float(recurring_ratio) * 25), 15)
        score -= min(int(volatility / 1000), 10)
        score += min(int(goal_progress / 10), 15)
        score = max(0, min(100, score))
        drivers = [
            f'Net balance: {net.quantize(Decimal("0.01"))}',
            f'Essential expense share: {(essential_ratio * Decimal("100")).quantize(Decimal("0.01"))}%',
            f'Recurring burden: {(recurring_ratio * Decimal("100")).quantize(Decimal("0.01"))}%',
            f'Goal progress average: {goal_progress:.1f}%',
        ]
        improvements = []
        if essential_ratio > Decimal('0.5'):
            improvements.append('Reduce essential expenses share below 50% of income.')
        if recurring_ratio > Decimal('0.2'):
            improvements.append('Audit subscriptions and recurring bills to lower fixed burden.')
        if net <= 0:
            improvements.append('Increase monthly free cash flow to restore a positive balance.')
        if not improvements:
            improvements.append('Maintain current pace and keep redirecting surplus into goals.')
        summary = 'Stable' if score >= 75 else 'Watchlist' if score >= 50 else 'At risk'
        return {'score': score, 'summary': summary, 'drivers': drivers, 'improvements': improvements}

    @staticmethod
    def _sum_direction(transactions: list[Transaction], direction: str) -> Decimal:
        return sum((tx.amount for tx in transactions if tx.direction == direction), Decimal('0.00')).quantize(Decimal('0.01'))

    @staticmethod
    def _daily_spend(transactions: list[Transaction]) -> dict[date, Decimal]:
        result: dict[date, Decimal] = defaultdict(lambda: Decimal('0'))
        for tx in transactions:
            if tx.direction == 'expense':
                result[tx.date] += tx.amount
        return result
