from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.bank_connection_repository import BankConnectionRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.import_repository import ImportSessionRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.analytics_service import AnalyticsService
from app.services.categorization_service import CategorizationService
from app.services.dashboard_service import DashboardService
from app.services.goal_service import GoalService
from app.services.import_service import ImportService
from app.services.integration_service import IntegrationService
from app.services.settings_service import SettingsService


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(TransactionRepository(db), GoalRepository(db))


def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(TransactionRepository(db), GoalRepository(db))


def get_import_service(db: Session = Depends(get_db)) -> ImportService:
    category_repository = CategoryRepository(db)
    categorization = CategorizationService(category_repository)
    return ImportService(ImportSessionRepository(db), TransactionRepository(db), categorization)


def get_integration_service(db: Session = Depends(get_db)) -> IntegrationService:
    category_repository = CategoryRepository(db)
    categorization = CategorizationService(category_repository)
    return IntegrationService(ImportSessionRepository(db), TransactionRepository(db), categorization)


def get_goal_service(db: Session = Depends(get_db)) -> GoalService:
    return GoalService(GoalRepository(db))


def get_settings_service(db: Session = Depends(get_db)) -> SettingsService:
    return SettingsService(BankConnectionRepository(db))
