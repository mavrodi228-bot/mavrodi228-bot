from app.schemas.common import ORMModel


class CategoryRead(ORMModel):
    id: int
    name: str
    slug: str
    icon: str
    color: str
    type: str
    parent_id: int | None = None
