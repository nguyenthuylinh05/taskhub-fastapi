from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.tasks import router as task_router
from app.core.database import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router
from app.api.v1.workspaces import router as workspace_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("TaskHub starting...")

    yield

    await engine.dispose()

    print("TaskHub shutting down...")


app = FastAPI(
    title="TaskHub API",
    description="Task Management API",
    version="2.0.0",
    lifespan=lifespan,
)


app.include_router(
    task_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    user_router,
    prefix="/api/v1",
)

app.include_router(
    workspace_router,
    prefix="/api/v1",
)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Welcome to TaskHub API"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
