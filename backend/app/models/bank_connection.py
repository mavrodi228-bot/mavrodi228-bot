from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.mixins import TimestampMixin


class BankConnection(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    provider_name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    auth_type: Mapped[str] = mapped_column(String(50), nullable=False)
    encrypted_credentials_json: Mapped[str] = mapped_column(Text, nullable=False)
