from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


class TaskRepository:
    def __init__(self):
        self.tasks: dict[int, TaskResponse] = {}
        self.next_id = 1

    def create(self, data: TaskCreate) -> TaskResponse:
        task = TaskResponse(
            id=self.next_id,
            **data.model_dump(),
        )

        self.tasks[task.id] = task
        self.next_id += 1
        return task

    def get_all(self) -> list[TaskResponse]:
        return list(self.tasks.values())

    def get_by_id(self, task_id: int) -> TaskResponse | None:
        return self.tasks.get(task_id)

    def update(
        self, task_id: int, data: TaskUpdate
    ) -> TaskResponse | None:
        current = self.get_by_id(task_id)

        if current is None:
            return None

        changes = data.model_dump(exclude_unset=True)

        updated = current.model_copy(update=changes)
        self.tasks[task_id] = updated

        return updated

    def delete(self, task_id: int) -> bool:
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        return True
