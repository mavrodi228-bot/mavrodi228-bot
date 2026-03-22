from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class CategoryRule(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str | None] = mapped_column(String(120))
    merchant_pattern: Mapped[str | None] = mapped_column(String(120))
    mcc: Mapped[str | None] = mapped_column(String(8))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    category: Mapped['Category'] = relationship()
