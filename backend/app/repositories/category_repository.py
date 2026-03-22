from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.category_rule import CategoryRule


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_categories(self) -> list[Category]:
        return list(self.db.scalars(select(Category).order_by(Category.type, Category.name)))

    def list_rules(self) -> list[CategoryRule]:
        stmt = select(CategoryRule).where(CategoryRule.is_active.is_(True)).order_by(CategoryRule.priority.asc())
        return list(self.db.scalars(stmt))

    def get_by_slug(self, slug: str) -> Category | None:
        return self.db.scalar(select(Category).where(Category.slug == slug))
