from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


CATEGORY_TYPES = ('income', 'expense', 'transfer', 'system')


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    icon: Mapped[str] = mapped_column(String(50), default='wallet')
    color: Mapped[str] = mapped_column(String(20), default='#64748b')
    type: Mapped[str] = mapped_column(Enum(*CATEGORY_TYPES, name='category_type'), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'))

    parent: Mapped['Category | None'] = relationship(remote_side='Category.id')
