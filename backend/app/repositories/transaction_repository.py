from datetime import date
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, joinedload
from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_transactions(
        self,
        date_from: date | None = None,
        date_to: date | None = None,
        category_id: int | None = None,
        search: str | None = None,
    ) -> list[Transaction]:
        stmt = select(Transaction).options(joinedload(Transaction.category)).where(Transaction.is_hidden.is_(False))
        if date_from:
            stmt = stmt.where(Transaction.date >= date_from)
        if date_to:
            stmt = stmt.where(Transaction.date <= date_to)
        if category_id:
            stmt = stmt.where(Transaction.category_id == category_id)
        if search:
            term = f'%{search.lower()}%'
            stmt = stmt.where(
                or_(
                    func.lower(Transaction.description).like(term),
                    func.lower(func.coalesce(Transaction.merchant, '')).like(term),
                )
            )
        return list(self.db.scalars(stmt.order_by(Transaction.date.desc(), Transaction.id.desc())))

    def add_all(self, transactions: list[Transaction]) -> None:
        self.db.add_all(transactions)

    def exists_duplicate(self, external_id: str | None, tx_date: date, amount, description: str) -> bool:
        conditions = [Transaction.date == tx_date, Transaction.amount == amount, Transaction.description == description]
        if external_id:
            conditions.append(Transaction.external_id == external_id)
            stmt = select(Transaction.id).where(or_(Transaction.external_id == external_id, and_(*conditions)))
        else:
            stmt = select(Transaction.id).where(and_(*conditions))
        return self.db.scalar(stmt) is not None

    def update_category(self, transaction_id: int, category_id: int | None) -> Transaction | None:
        transaction = self.db.get(Transaction, transaction_id)
        if not transaction:
            return None
        transaction.category_id = category_id
        self.db.add(transaction)
        self.db.flush()
        self.db.refresh(transaction)
        return transaction

    def month_transactions(self, month_start: date, month_end: date) -> list[Transaction]:
        stmt = select(Transaction).options(joinedload(Transaction.category)).where(
            Transaction.date >= month_start,
            Transaction.date <= month_end,
            Transaction.is_hidden.is_(False),
        )
        return list(self.db.scalars(stmt.order_by(Transaction.date.asc())))
