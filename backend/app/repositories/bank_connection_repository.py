from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.bank_connection import BankConnection


class BankConnectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[BankConnection]:
        return list(self.db.scalars(select(BankConnection).order_by(BankConnection.created_at.desc())))

    def create(self, connection: BankConnection) -> BankConnection:
        self.db.add(connection)
        self.db.flush()
        self.db.refresh(connection)
        return connection
