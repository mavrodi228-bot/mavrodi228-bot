from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_goal_service
from app.schemas.goal import GoalCreate, GoalRead, GoalUpdate

router = APIRouter(prefix='/goals', tags=['goals'])


@router.get('', response_model=list[GoalRead])
def list_goals(service=Depends(get_goal_service)) -> list[GoalRead]:
    return service.list()


@router.post('', response_model=GoalRead)
def create_goal(payload: GoalCreate, service=Depends(get_goal_service)) -> GoalRead:
    goal = service.create(payload)
    service.repository.db.commit()
    return goal


@router.patch('/{goal_id}', response_model=GoalRead)
def update_goal(goal_id: int, payload: GoalUpdate, service=Depends(get_goal_service)) -> GoalRead:
    goal = service.update(goal_id, payload)
    if not goal:
        raise HTTPException(status_code=404, detail='Goal not found')
    service.repository.db.commit()
    return goal
