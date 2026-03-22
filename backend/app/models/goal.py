from datetime import date
from decimal import Decimal
from sqlalchemy import Date, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.mixins import TimestampMixin


GOAL_STATUS = ('active', 'completed', 'paused')


class Goal(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    target_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    current_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    deadline: Mapped[date | None] = mapped_column(Date)
    monthly_target: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    status: Mapped[str] = mapped_column(Enum(*GOAL_STATUS, name='goal_status'), default='active', nullable=False)
