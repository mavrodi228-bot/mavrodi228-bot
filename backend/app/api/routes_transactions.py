from datetime import date
from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session
from app.api.deps import get_import_service
from app.db.session import get_db
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.common import ImportResult
from app.schemas.transaction import TransactionRead, TransactionUpdateCategory

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.get('', response_model=list[TransactionRead])
def list_transactions(
    date_from: date | None = None,
    date_to: date | None = None,
    category_id: int | None = None,
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[TransactionRead]:
    repo = TransactionRepository(db)
    return [TransactionRead.model_validate(item) for item in repo.list_transactions(date_from, date_to, category_id, search)]


@router.patch('/{transaction_id}/category', response_model=TransactionRead)
def update_category(transaction_id: int, payload: TransactionUpdateCategory, db: Session = Depends(get_db)) -> TransactionRead:
    transaction = TransactionRepository(db).update_category(transaction_id, payload.category_id)
    db.commit()
    return TransactionRead.model_validate(transaction)


@router.post('/import/csv', response_model=ImportResult)
async def import_csv(file: UploadFile = File(...), service=Depends(get_import_service)) -> ImportResult:
    content = await file.read()
    result = service.import_tbank_file(file.filename or 'statement.csv', content)
    service.transaction_repository.db.commit()
    return result


@router.post('/import/xlsx', response_model=ImportResult)
async def import_xlsx(file: UploadFile = File(...), service=Depends(get_import_service)) -> ImportResult:
    content = await file.read()
    result = service.import_tbank_file(file.filename or 'statement.xlsx', content)
    service.transaction_repository.db.commit()
    return result
