PYTHON=python3
PIP=$(PYTHON) -m pip

install:
	$(PIP) install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	PYTHONPATH=. pytest

migrate:
	alembic upgrade head
