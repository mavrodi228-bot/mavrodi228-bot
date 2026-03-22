from datetime import date
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.deps import get_integration_service
from app.schemas.common import ImportResult

router = APIRouter(prefix='/integrations/tbank-business', tags=['integrations'])


class SyncPayload(BaseModel):
    date_from: date
    date_to: date


@router.post('/sync', response_model=ImportResult)
def sync_tbank_business(payload: SyncPayload, service=Depends(get_integration_service)) -> ImportResult:
    result = service.sync_tbank_business(payload.date_from, payload.date_to)
    service.transaction_repository.db.commit()
    return result
