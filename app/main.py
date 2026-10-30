from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.tasks import router as task_router
from app.repositories.task_repository import TaskRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Chạy khi ứng dụng khởi động
    print("TaskHub starting...")

    app.state.task_repository = TaskRepository()

    yield

    # Chạy khi ứng dụng dừng
    print("TaskHub shutting down...")


app = FastAPI(
    title="TaskHub API",
    description="Task Management API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(
    task_router,
    prefix="/api/v1",
)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Welcome to TaskHub API"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
