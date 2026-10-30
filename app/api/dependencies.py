from typing import Annotated

from fastapi import Depends, Request

from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def get_task_repository(request: Request) -> TaskRepository:
    return request.app.state.task_repository


def get_task_service(
    repository: Annotated[
        TaskRepository, Depends(get_task_repository)
    ],
) -> TaskService:
    return TaskService(repository)


TaskServiceDep = Annotated[
    TaskService, Depends(get_task_service)
]
