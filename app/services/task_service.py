from fastapi import HTTPException, status
from app.models.user import User

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

    async def create_task(
        self,
        data: TaskCreate,
        current_user: User,
    ):
        task_data = data.model_dump(mode="json")
        task_data["user_id"] = current_user.id

        return await self.repository.create(task_data)

    async def list_tasks(
        self,
        pagination: PaginationParams,
        current_user: User,
    ):
        items = await self.repository.get_all_for_user(
            user_id=current_user.id,
            skip=pagination.skip,
            limit=pagination.page_size,
        )

        total = await self.repository.count_for_user(
            user_id=current_user.id,
        )

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

    async def get_task(self, task_id: int, current_user: User):
        task = await self.repository.get_by_id_for_user(
            task_id=task_id,
            user_id=current_user.id,
        )

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
        current_user: User,
    ):
        task = await self.get_task(task_id, current_user)

        changes = data.model_dump(
            mode="json",
            exclude_unset=True,
        )

        return await self.repository.update(task, changes)

    async def delete_task(self, task_id: int, current_user: User):
        task = await self.get_task(task_id, current_user)
        await self.repository.delete(task)
