from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_analytics, routes_categories, routes_dashboard, routes_goals, routes_health, routes_integrations, routes_recommendations, routes_settings, routes_transactions
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

for router in [
    routes_health.router,
    routes_dashboard.router,
    routes_transactions.router,
    routes_integrations.router,
    routes_categories.router,
    routes_analytics.router,
    routes_goals.router,
    routes_recommendations.router,
    routes_settings.router,
]:
    app.include_router(router, prefix=settings.api_prefix)


@app.get('/')
def root() -> dict[str, str]:
    return {'message': 'CashLens API'}
