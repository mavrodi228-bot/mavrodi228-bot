from datetime import timedelta
from app.models.goal import Goal
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal import GoalCreate, GoalRead, GoalUpdate


class GoalService:
    def __init__(self, repository: GoalRepository):
        self.repository = repository

    def list(self) -> list[GoalRead]:
        return [self._enrich(goal) for goal in self.repository.list()]

    def create(self, payload: GoalCreate) -> GoalRead:
        goal = self.repository.create(Goal(**payload.model_dump()))
        return self._enrich(goal)

    def update(self, goal_id: int, payload: GoalUpdate) -> GoalRead | None:
        goal = self.repository.get(goal_id)
        if not goal:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(goal, field, value)
        self.repository.db.add(goal)
        self.repository.db.flush()
        self.repository.db.refresh(goal)
        return self._enrich(goal)

    def _enrich(self, goal: Goal) -> GoalRead:
        progress = float((goal.current_amount / goal.target_amount) * 100) if goal.target_amount else 0.0
        estimated = None
        if goal.monthly_target and goal.monthly_target > 0 and progress < 100:
            months_left = max(int((goal.target_amount - goal.current_amount) / goal.monthly_target), 0)
            estimated = (goal.deadline or goal.created_at.date()) + timedelta(days=30 * months_left)
        data = GoalRead.model_validate(goal)
        data.progress_percent = round(progress, 2)
        data.estimated_completion_date = estimated
        return data
