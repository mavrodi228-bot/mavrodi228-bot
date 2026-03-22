from pathlib import Path
from app.importers.tbank_csv_importer import TBankCsvImporter


def test_parse_tbank_csv_fixture():
    fixture_path = Path(__file__).parents[1] / 'fixtures' / 'tbank_statement.csv'
    importer = TBankCsvImporter()
    parsed = importer.parse(fixture_path.name, fixture_path.read_bytes())
    assert len(parsed.transactions) == 3
    assert parsed.transactions[0].merchant == 'Пятерочка'
    assert parsed.transactions[1].direction == 'expense'
    assert parsed.transactions[2].direction == 'income'
