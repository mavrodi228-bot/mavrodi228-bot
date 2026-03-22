from datetime import date, datetime, timezone
from app.integrations.tbank_business_provider import TBankBusinessProvider
from app.models.import_session import ImportSession
from app.repositories.import_repository import ImportSessionRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.categorization_service import CategorizationService
from app.schemas.common import ImportResult


class IntegrationService:
    def __init__(
        self,
        import_repository: ImportSessionRepository,
        transaction_repository: TransactionRepository,
        categorization_service: CategorizationService,
        provider: TBankBusinessProvider | None = None,
    ):
        self.import_repository = import_repository
        self.transaction_repository = transaction_repository
        self.categorization_service = categorization_service
        self.provider = provider or TBankBusinessProvider()

    def sync_tbank_business(self, date_from: date, date_to: date) -> ImportResult:
        session = self.import_repository.create(ImportSession(source_type='tbank_business_api', status='processing'))
        result = self.provider.sync_transactions(date_from, date_to)
        imported = 0
        skipped = 0
        for transaction in result.transactions:
            if self.transaction_repository.exists_duplicate(
                transaction.external_id, transaction.date, transaction.amount, transaction.description
            ):
                skipped += 1
                continue
            transaction.category_id = self.categorization_service.categorize(transaction)
            self.transaction_repository.add_all([transaction])
            imported += 1
        session.imported_rows = imported
        session.skipped_rows = skipped
        session.finished_at = datetime.now(timezone.utc)
        session.status = 'completed'
        return ImportResult(imported_rows=imported, skipped_rows=skipped, errors=[])
