from sqlalchemy.orm import Session
from app.models.import_session import ImportSession


class ImportSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, session: ImportSession) -> ImportSession:
        self.db.add(session)
        self.db.flush()
        self.db.refresh(session)
        return session
