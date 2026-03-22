from fastapi import APIRouter, Depends
from app.api.deps import get_dashboard_service
from app.schemas.dashboard import DashboardSummary
from app.schemas.common import ChartPoint, MoneyPoint

router = APIRouter(prefix='/dashboard', tags=['dashboard'])


@router.get('/summary', response_model=DashboardSummary)
def dashboard_summary(service=Depends(get_dashboard_service)) -> DashboardSummary:
    return service.summary()


@router.get('/charts/monthly', response_model=dict[str, list])
def dashboard_charts(service=Depends(get_dashboard_service)) -> dict[str, list[ChartPoint | MoneyPoint]]:
    summary = service.summary()
    return {
        'daily_spend_chart': summary.daily_spend_chart,
        'category_share_chart': summary.category_share_chart,
        'top_expense_categories': summary.top_expense_categories,
    }
