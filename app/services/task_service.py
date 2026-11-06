
from fastapi import HTTPException, status

from app.repositories.task_repository import TaskRepository
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.schemas.pagination import (
    PaginationParams,
    PaginatedResponse,
)


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, data: TaskCreate):
        return await self.repository.create(
            data.model_dump(mode="json")
        )

    async def list_tasks(
        self,
        pagination: PaginationParams,
    ):
        items = await self.repository.get_all(
            skip=pagination.skip,
            limit=pagination.page_size,
        )

        total = await self.repository.count()

        return PaginatedResponse[TaskResponse](
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=(
                (total + pagination.page_size - 1)
                // pagination.page_size
            ),
        )

    async def get_task(self, task_id: int):
        task = await self.repository.get_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    async def update_task(
        self,
        task_id: int,
        data: TaskUpdate,
    ):
        task = await self.get_task(task_id)

        changes = data.model_dump(
            mode="json",
            exclude_unset=True,
        )

        return await self.repository.update(task, changes)

    async def delete_task(self, task_id: int):
        task = await self.get_task(task_id)

        await self.repository.delete(task)
