from decimal import Decimal
from datetime import date, timedelta
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.category import Category
from app.models.goal import Goal
from app.models.transaction import Transaction


def seed_demo() -> None:
    db = SessionLocal()
    try:
        if db.scalar(select(Transaction.id).limit(1)):
            return
        categories = {category.slug: category for category in db.scalars(select(Category))}
        today = date.today().replace(day=15)
        demo_transactions = [
            Transaction(source_type='manual', date=today.replace(day=1), amount=Decimal('120000'), currency='RUB', direction='income', description='Salary March', merchant='Acme Corp', category_id=categories['salary'].id),
            Transaction(source_type='manual', date=today.replace(day=2), amount=Decimal('4500'), currency='RUB', direction='expense', description='Яндекс Аренда', merchant='Yandex Rent', category_id=categories['housing'].id),
            Transaction(source_type='manual', date=today.replace(day=3), amount=Decimal('2300'), currency='RUB', direction='expense', description='Пятерочка', merchant='Пятерочка', category_id=categories['groceries'].id),
            Transaction(source_type='manual', date=today.replace(day=5), amount=Decimal('999'), currency='RUB', direction='expense', description='Netflix', merchant='Netflix', category_id=categories['subscriptions'].id, is_recurring=True),
            Transaction(source_type='manual', date=today.replace(day=7), amount=Decimal('690'), currency='RUB', direction='expense', description='Surf Coffee', merchant='Surf Coffee', category_id=categories['other'].id),
            Transaction(source_type='manual', date=today.replace(day=8), amount=Decimal('850'), currency='RUB', direction='expense', description='Yandex Go', merchant='Yandex Go', category_id=categories['taxi'].id),
            Transaction(source_type='manual', date=today.replace(day=12), amount=Decimal('3100'), currency='RUB', direction='expense', description='Ozon order', merchant='Ozon', category_id=categories['marketplaces'].id),
            Transaction(source_type='manual', date=today.replace(day=14), amount=Decimal('760'), currency='RUB', direction='expense', description='Metro', merchant='Metro', category_id=categories['transport'].id),
        ]
        db.add_all(demo_transactions)
        db.add(Goal(title='Emergency Fund', target_amount=Decimal('300000'), current_amount=Decimal('90000'), monthly_target=Decimal('25000'), deadline=today + timedelta(days=240), status='active'))
        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    seed_demo()
