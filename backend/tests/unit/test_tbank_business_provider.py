from datetime import date
import httpx
from app.integrations.tbank_business_provider import TBankBusinessProvider


def test_sync_transactions_normalizes_response(monkeypatch):
    def handler(request):
        return httpx.Response(200, json={
            'items': [
                {
                    'id': 'op_1',
                    'accountId': 'acc_1',
                    'operationDate': '2026-03-05',
                    'amount': '-1599.90',
                    'currency': 'RUB',
                    'description': 'Yandex Go ride',
                    'counterpartyName': 'Yandex Go',
                    'type': 'payment',
                    'mcc': '4121',
                }
            ]
        })
    transport = httpx.MockTransport(handler)
    provider = TBankBusinessProvider(client=httpx.Client(transport=transport, base_url='https://example.com'))
    monkeypatch.setattr(provider.settings, 'tbank_business_token', 'token')
    result = provider.sync_transactions(date(2026, 3, 1), date(2026, 3, 10))
    assert len(result.transactions) == 1
    transaction = result.transactions[0]
    from decimal import Decimal
    assert transaction.amount == Decimal('1599.90')
    assert transaction.direction == 'expense'
    assert transaction.external_id == 'op_1'
