from datetime import datetime, timezone
from fastapi import APIRouter
from app.schemas.common import HealthResponse

router = APIRouter(prefix='/health', tags=['health'])


@router.get('', response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status='ok', timestamp=datetime.now(timezone.utc))
