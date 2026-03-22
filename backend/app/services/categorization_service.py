from app.models.transaction import Transaction
from app.repositories.category_repository import CategoryRepository


class CategorizationService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def categorize(self, transaction: Transaction) -> int | None:
        description = (transaction.description or '').lower()
        merchant = (transaction.merchant or '').lower()
        rules = self.category_repository.list_rules()
        fallback = self.category_repository.get_by_slug('other')

        for rule in rules:
            if rule.mcc and transaction.mcc and rule.mcc == transaction.mcc:
                return rule.category_id
            if rule.keyword and rule.keyword.lower() in description:
                return rule.category_id
            if rule.merchant_pattern and rule.merchant_pattern.lower() in merchant:
                return rule.category_id
        return fallback.id if fallback else None
