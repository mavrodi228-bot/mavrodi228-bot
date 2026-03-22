from fastapi import APIRouter, Depends
from app.api.deps import get_settings_service
from app.schemas.bank_connection import BankConnectionCreate, BankConnectionRead

router = APIRouter(prefix='/settings/bank-connections', tags=['settings'])


@router.get('', response_model=list[BankConnectionRead])
def list_connections(service=Depends(get_settings_service)) -> list[BankConnectionRead]:
    return service.list_connections()


@router.post('', response_model=BankConnectionRead)
def create_connection(payload: BankConnectionCreate, service=Depends(get_settings_service)) -> BankConnectionRead:
    connection = service.create_connection(payload)
    service.repository.db.commit()
    return connection
