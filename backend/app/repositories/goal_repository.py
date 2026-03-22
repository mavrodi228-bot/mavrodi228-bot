from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.goal import Goal


class GoalRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Goal]:
        return list(self.db.scalars(select(Goal).order_by(Goal.created_at.desc())))

    def create(self, goal: Goal) -> Goal:
        self.db.add(goal)
        self.db.flush()
        self.db.refresh(goal)
        return goal

    def get(self, goal_id: int) -> Goal | None:
        return self.db.get(Goal, goal_id)
