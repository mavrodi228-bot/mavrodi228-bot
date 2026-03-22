from dataclasses import dataclass
from datetime import date
from decimal import Decimal
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from app.core.config import get_settings
from app.models.transaction import Transaction
from app.utils.normalization import extract_merchant, sanitize_text


class TBankBusinessProviderError(RuntimeError):
    pass


@dataclass
class SyncResult:
    transactions: list[Transaction]
    raw_payload: dict


class TBankBusinessProvider:
    def __init__(self, client: httpx.Client | None = None):
        self.settings = get_settings()
        self.client = client or httpx.Client(
            base_url=self.settings.tbank_business_base_url,
            timeout=self.settings.tbank_business_timeout_seconds,
        )

    def _headers(self) -> dict[str, str]:
        if not self.settings.tbank_business_token:
            raise TBankBusinessProviderError('T-Bank Business token is not configured')
        return {'Authorization': f'Bearer {self.settings.tbank_business_token}'}

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError, TBankBusinessProviderError)),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def sync_transactions(self, date_from: date, date_to: date) -> SyncResult:
        params = {
            'accountId': self.settings.tbank_business_account_id,
            'companyId': self.settings.tbank_business_company_id,
            'from': date_from.isoformat(),
            'to': date_to.isoformat(),
        }
        response = self.client.get('/statements', params=params, headers=self._headers())
        response.raise_for_status()
        payload = response.json()
        if 'items' not in payload:
            raise TBankBusinessProviderError('Unexpected statement response format')
        return SyncResult(transactions=[self._normalize_item(item) for item in payload['items']], raw_payload=payload)

    def _normalize_item(self, item: dict) -> Transaction:
        amount = Decimal(str(item.get('amount', 0))).quantize(Decimal('0.01'))
        direction = 'income' if amount >= 0 else 'expense'
        description = sanitize_text(item.get('description') or item.get('purpose') or 'T-Bank transaction')
        return Transaction(
            external_id=str(item.get('id') or item.get('operationId') or ''),
            source_type='tbank_business_api',
            account_id=str(item.get('accountId') or self.settings.tbank_business_account_id or ''),
            date=date.fromisoformat(item.get('operationDate', date.today().isoformat())[:10]),
            amount=abs(amount),
            currency=item.get('currency', 'RUB'),
            direction=direction,
            description=description,
            merchant=extract_merchant(item.get('counterpartyName') or description),
            mcc=str(item.get('mcc')) if item.get('mcc') else None,
            raw_category=item.get('categoryName'),
            is_transfer=item.get('type') == 'transfer',
        )
