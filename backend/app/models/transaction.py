from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin


SOURCE_TYPES = ('tbank_business_api', 'tbank_csv', 'manual', 'future')
DIRECTIONS = ('income', 'expense', 'transfer', 'refund')


class Transaction(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(255), index=True)
    source_type: Mapped[str] = mapped_column(Enum(*SOURCE_TYPES, name='source_type'), nullable=False)
    account_id: Mapped[str | None] = mapped_column(String(255), index=True)
    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), default='RUB', nullable=False)
    direction: Mapped[str] = mapped_column(Enum(*DIRECTIONS, name='transaction_direction'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    merchant: Mapped[str | None] = mapped_column(String(255), index=True)
    mcc: Mapped[str | None] = mapped_column(String(8), index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'), index=True)
    raw_category: Mapped[str | None] = mapped_column(String(120))
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    category: Mapped['Category | None'] = relationship()
