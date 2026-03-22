from dataclasses import dataclass
from io import BytesIO, StringIO
import pandas as pd
from app.models.transaction import Transaction
from app.utils.normalization import extract_merchant, normalize_amount, normalize_date, sanitize_text


@dataclass
class ParsedImport:
    transactions: list[Transaction]
    columns: list[str]


class TBankCsvImporter:
    COLUMN_ALIASES = {
        'date': ['date', 'operation date', 'дата', 'дата операции'],
        'amount': ['amount', 'sum', 'сумма', 'amount rub'],
        'description': ['description', 'details', 'описание', 'назначение'],
        'currency': ['currency', 'валюта'],
        'mcc': ['mcc'],
        'external_id': ['id', 'operation id', 'external_id'],
    }

    def parse(self, file_name: str, content: bytes) -> ParsedImport:
        dataframe = self._load_dataframe(file_name, content)
        mapping = self._detect_mapping(dataframe.columns)
        transactions: list[Transaction] = []
        for row in dataframe.to_dict(orient='records'):
            description = sanitize_text(row.get(mapping['description'], ''))
            amount_value = normalize_amount(row.get(mapping['amount'], 0))
            direction = 'income' if amount_value >= 0 else 'expense'
            transactions.append(
                Transaction(
                    external_id=str(row.get(mapping.get('external_id'), '') or '') or None,
                    source_type='tbank_csv',
                    account_id=None,
                    date=normalize_date(row.get(mapping['date'])).date(),
                    amount=abs(amount_value),
                    currency=sanitize_text(str(row.get(mapping.get('currency'), 'RUB') or 'RUB')),
                    direction=direction,
                    description=description,
                    merchant=extract_merchant(description),
                    mcc=sanitize_text(str(row.get(mapping.get('mcc'), '') or '')) or None,
                    raw_category=None,
                    is_transfer='перевод' in description.lower() or 'transfer' in description.lower(),
                )
            )
        return ParsedImport(transactions=transactions, columns=[str(column) for column in dataframe.columns])

    def _load_dataframe(self, file_name: str, content: bytes) -> pd.DataFrame:
        lower_name = file_name.lower()
        if lower_name.endswith('.csv'):
            text = content.decode('utf-8-sig')
            return pd.read_csv(StringIO(text))
        if lower_name.endswith('.xlsx'):
            return pd.read_excel(BytesIO(content))
        raise ValueError('Unsupported file format; only CSV and XLSX are supported')

    def _detect_mapping(self, columns) -> dict[str, str]:
        normalized = {str(column).strip().lower(): str(column) for column in columns}
        mapping: dict[str, str] = {}
        for field, aliases in self.COLUMN_ALIASES.items():
            for alias in aliases:
                if alias in normalized:
                    mapping[field] = normalized[alias]
                    break
        required = {'date', 'amount', 'description'}
        missing = required - set(mapping)
        if missing:
            raise ValueError(f'Missing required columns: {", ".join(sorted(missing))}')
        return mapping
