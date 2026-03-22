from datetime import datetime
from sqlalchemy import DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


IMPORT_STATUS = ('pending', 'processing', 'completed', 'failed')
IMPORT_SOURCES = ('tbank_business_api', 'tbank_csv', 'manual', 'future')


class ImportSession(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    source_type: Mapped[str] = mapped_column(Enum(*IMPORT_SOURCES, name='import_source_type'), nullable=False)
    file_name: Mapped[str | None] = mapped_column(String(255))
    imported_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    skipped_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(Enum(*IMPORT_STATUS, name='import_status'), default='pending', nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)
