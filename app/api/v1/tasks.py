from fastapi import APIRouter, status

from app.api.dependencies import TaskServiceDep
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    service: TaskServiceDep,
):
    return service.create_task(data)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(service: TaskServiceDep):
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskServiceDep,
):
    return service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    service: TaskServiceDep,
):
    return service.update_task(task_id, data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    service: TaskServiceDep,
):
    service.delete_task(task_id)
