from fastapi import HTTPException, status

from app.repositories.task_repository import TaskRepository
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, data: TaskCreate) -> TaskResponse:
        return self.repository.create(data)

    def list_tasks(self) -> list[TaskResponse]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> TaskResponse:
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    def update_task(
        self, task_id: int, data: TaskUpdate
    ) -> TaskResponse:
        self.get_task(task_id)
        updated = self.repository.update(task_id, data)

        if updated is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        return updated

    def delete_task(self, task_id: int) -> None:
        deleted = self.repository.delete(task_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )
