from fastapi import APIRouter, Depends
from app.api.deps import get_analytics_service
from app.schemas.analytics import AnalyticsOverview, CategoryAnalyticsRead, ForecastRead, RecommendationsRead, RecurringPaymentRead

router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.get('/overview', response_model=AnalyticsOverview)
def overview(service=Depends(get_analytics_service)) -> AnalyticsOverview:
    return service.overview()


@router.get('/categories', response_model=CategoryAnalyticsRead)
def categories(service=Depends(get_analytics_service)) -> CategoryAnalyticsRead:
    return service.categories()


@router.get('/recurring', response_model=list[RecurringPaymentRead])
def recurring(service=Depends(get_analytics_service)) -> list[RecurringPaymentRead]:
    return service.recurring()


@router.get('/forecast', response_model=ForecastRead)
def forecast(service=Depends(get_analytics_service)) -> ForecastRead:
    return service.forecast()
