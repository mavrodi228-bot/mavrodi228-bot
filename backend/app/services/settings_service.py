import json
from app.core.security import encrypt_text
from app.models.bank_connection import BankConnection
from app.repositories.bank_connection_repository import BankConnectionRepository
from app.schemas.bank_connection import BankConnectionCreate, BankConnectionRead


class SettingsService:
    def __init__(self, repository: BankConnectionRepository):
        self.repository = repository

    def list_connections(self) -> list[BankConnectionRead]:
        return [BankConnectionRead.model_validate(item) for item in self.repository.list()]

    def create_connection(self, payload: BankConnectionCreate) -> BankConnectionRead:
        connection = self.repository.create(
            BankConnection(
                provider_name=payload.provider_name,
                is_active=payload.is_active,
                auth_type=payload.auth_type,
                encrypted_credentials_json=encrypt_text(json.dumps(payload.credentials)),
            )
        )
        return BankConnectionRead.model_validate(connection)
