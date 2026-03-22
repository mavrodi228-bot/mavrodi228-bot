from decimal import Decimal
from datetime import date, timedelta
import pytest
from app.models.category import Category
from app.models.goal import Goal
from app.models.transaction import Transaction


@pytest.fixture
def categories():
    return {
        'groceries': Category(id=1, name='Groceries', slug='groceries', icon='basket', color='#10b981', type='expense'),
        'subscriptions': Category(id=2, name='Subscriptions', slug='subscriptions', icon='repeat', color='#8b5cf6', type='expense'),
        'salary': Category(id=3, name='Salary', slug='salary', icon='badge-russian-ruble', color='#22c55e', type='income'),
        'other': Category(id=4, name='Other', slug='other', icon='circle', color='#94a3b8', type='expense'),
    }


@pytest.fixture
def sample_transactions(categories):
    today = date.today().replace(day=15)
    return [
        Transaction(id=1, source_type='manual', date=today.replace(day=1), amount=Decimal('120000'), currency='RUB', direction='income', description='Salary March', merchant='Employer', category=categories['salary']),
        Transaction(id=2, source_type='manual', date=today.replace(day=2), amount=Decimal('1200'), currency='RUB', direction='expense', description='Пятерочка', merchant='Пятерочка', category=categories['groceries']),
        Transaction(id=3, source_type='manual', date=today.replace(day=3), amount=Decimal('999'), currency='RUB', direction='expense', description='Netflix', merchant='Netflix', category=categories['subscriptions']),
        Transaction(id=4, source_type='manual', date=today.replace(day=8), amount=Decimal('450'), currency='RUB', direction='expense', description='Coffee', merchant='Surf Coffee', category=categories['other']),
        Transaction(id=5, source_type='manual', date=today.replace(day=10), amount=Decimal('1300'), currency='RUB', direction='expense', description='Пятерочка', merchant='Пятерочка', category=categories['groceries']),
        Transaction(id=6, source_type='manual', date=today.replace(day=12), amount=Decimal('999'), currency='RUB', direction='expense', description='Netflix', merchant='Netflix', category=categories['subscriptions']),
    ]


@pytest.fixture
def previous_transactions(categories):
    previous_day = date.today().replace(day=1) - timedelta(days=1)
    return [
        Transaction(id=10, source_type='manual', date=previous_day.replace(day=5), amount=Decimal('3000'), currency='RUB', direction='expense', description='Previous grocery', merchant='Пятерочка', category=categories['groceries']),
    ]


@pytest.fixture
def goals():
    return [Goal(id=1, title='Emergency Fund', target_amount=Decimal('300000'), current_amount=Decimal('90000'), monthly_target=Decimal('25000'), status='active')]
