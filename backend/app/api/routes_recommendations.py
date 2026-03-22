from fastapi import APIRouter, Depends
from app.api.deps import get_analytics_service
from app.schemas.analytics import RecommendationsRead

router = APIRouter(prefix='/recommendations', tags=['recommendations'])


@router.get('', response_model=RecommendationsRead)
def recommendations(service=Depends(get_analytics_service)) -> RecommendationsRead:
    return service.recommendations()
