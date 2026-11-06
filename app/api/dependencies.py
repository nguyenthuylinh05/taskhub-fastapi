
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


DBSession = Annotated[
    AsyncSession,
    Depends(get_db),
]


def get_task_repository(
    db: DBSession,
) -> TaskRepository:
    return TaskRepository(db)


def get_task_service(
    repository: Annotated[
        TaskRepository,
        Depends(get_task_repository),
    ],
) -> TaskService:
    return TaskService(repository)


TaskServiceDep = Annotated[
    TaskService,
    Depends(get_task_service),
]
