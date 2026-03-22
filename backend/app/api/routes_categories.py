from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryRead

router = APIRouter(prefix='/categories', tags=['categories'])


@router.get('', response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:
    return [CategoryRead.model_validate(item) for item in CategoryRepository(db).list_categories()]
