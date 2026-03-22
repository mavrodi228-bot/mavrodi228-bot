import re
from datetime import datetime
from decimal import Decimal
from dateutil import parser


def sanitize_text(value: str | None) -> str:
    if not value:
        return ''
    return re.sub(r'\s+', ' ', value).strip()


def normalize_amount(raw) -> Decimal:
    if isinstance(raw, Decimal):
        return raw.quantize(Decimal('0.01'))
    cleaned = str(raw).replace(' ', '').replace(' ', '').replace(',', '.')
    return Decimal(cleaned).quantize(Decimal('0.01'))


def normalize_date(raw) -> datetime:
    if isinstance(raw, datetime):
        return raw
    return parser.parse(str(raw), dayfirst=True)


def extract_merchant(description: str) -> str:
    value = sanitize_text(description)
    parts = re.split(r'[/|,-]', value)
    merchant = parts[0].strip() if parts else value
    return merchant[:255]
