from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.dependencies import TaskServiceDep
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.schemas.pagination import (
    PaginationParams,
    PaginatedResponse,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    service: TaskServiceDep,
):
    return await service.create_task(data)


@router.get(
    "",
    response_model=PaginatedResponse[TaskResponse],
)
async def list_tasks(
    service: TaskServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    pagination = PaginationParams(
        page=page,
        page_size=page_size,
    )

    return await service.list_tasks(pagination)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskServiceDep,
):
    return await service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    service: TaskServiceDep,
):
    return await service.update_task(task_id, data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    service: TaskServiceDep,
):
    await service.delete_task(task_id)
