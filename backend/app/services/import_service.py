from datetime import datetime, timezone
from app.importers.tbank_csv_importer import TBankCsvImporter
from app.models.import_session import ImportSession
from app.repositories.import_repository import ImportSessionRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.categorization_service import CategorizationService
from app.schemas.common import ImportResult


class ImportService:
    def __init__(
        self,
        import_repository: ImportSessionRepository,
        transaction_repository: TransactionRepository,
        categorization_service: CategorizationService,
    ):
        self.import_repository = import_repository
        self.transaction_repository = transaction_repository
        self.categorization_service = categorization_service

    def import_tbank_file(self, file_name: str, content: bytes) -> ImportResult:
        session = self.import_repository.create(
            ImportSession(source_type='tbank_csv', file_name=file_name, status='processing')
        )
        importer = TBankCsvImporter()
        parsed = importer.parse(file_name=file_name, content=content)
        imported = 0
        skipped = 0
        errors: list[str] = []
        for transaction in parsed.transactions:
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
        return ImportResult(imported_rows=imported, skipped_rows=skipped, errors=errors)
