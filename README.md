# CashLens

CashLens is a production-like pet project for personal finance analytics with a realistic T-Bank integration strategy:
- **TBankBusinessProvider** for official T-Bank Business OpenAPI statement sync.
- **TBankCsvImporter** as a resilient fallback for CSV/XLSX retail statement imports.
- Clean modular FastAPI + React architecture with analytics, forecast, insights, and goals.

## Project tree

```text
.
├── backend
│   ├── alembic
│   │   ├── env.py
│   │   └── versions/20260322_0001_init.py
│   ├── app
│   │   ├── analytics
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── importers
│   │   ├── integrations
│   │   ├── models
│   │   ├── recommendations
│   │   ├── repositories
│   │   ├── schemas
│   │   ├── services
│   │   └── utils
│   ├── tests
│   ├── Dockerfile
│   ├── Makefile
│   └── requirements.txt
├── frontend
│   ├── src
│   │   ├── api
│   │   ├── app
│   │   ├── components
│   │   ├── hooks
│   │   ├── lib
│   │   ├── pages
│   │   └── types
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── Makefile
```

## Backend architecture

- **FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL**.
- Provider-based integration layer for bank sync.
- Import pipeline for CSV/XLSX with format detection, normalization, and deduplication.
- Rule-based categorization, recurring detection, recommendations, forecast, and custom Financial Stability Score.

## API endpoints

- `GET /api/health`
- `GET /api/dashboard/summary`
- `GET /api/dashboard/charts/monthly`
- `GET /api/transactions`
- `POST /api/transactions/import/csv`
- `POST /api/transactions/import/xlsx`
- `PATCH /api/transactions/{id}/category`
- `POST /api/integrations/tbank-business/sync`
- `GET /api/categories`
- `GET /api/analytics/overview`
- `GET /api/analytics/categories`
- `GET /api/analytics/recurring`
- `GET /api/analytics/forecast`
- `GET /api/goals`
- `POST /api/goals`
- `PATCH /api/goals/{id}`
- `GET /api/recommendations`
- `GET /api/settings/bank-connections`
- `POST /api/settings/bank-connections`

## Local development

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m app.db.seed_demo
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Full stack with Docker

```bash
make up
```

## T-Bank configuration

Set the following environment variables in `backend/.env` for the official business provider:

- `T_BANK_BUSINESS_BASE_URL`
- `T_BANK_BUSINESS_TOKEN`
- `T_BANK_BUSINESS_ACCOUNT_ID`
- `T_BANK_BUSINESS_COMPANY_ID`
- `ENCRYPTION_KEY`

If the official business API is not available for the use case, use the CSV/XLSX import flow. The app intentionally does **not** use any private or undocumented retail banking APIs.

## Demo data

`python -m app.db.seed_demo` inserts a salary, housing, groceries, subscriptions, taxi, marketplaces, and a sample goal so the dashboard is populated on first run.

## Testing

```bash
cd backend && PYTHONPATH=. pytest
cd frontend && npm run build
```
