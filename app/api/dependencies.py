from typing import Annotated
import jwt

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.database import AsyncSessionLocal
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.workspace_repository import WorkspaceRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.services.workspace_service import WorkspaceService

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


def get_user_repository(
    db: DBSession,
) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
]

def get_refresh_token_repository(
    db: DBSession,
) -> RefreshTokenRepository:
    return RefreshTokenRepository(db)


RefreshTokenRepositoryDep = Annotated[
    RefreshTokenRepository,
    Depends(get_refresh_token_repository),
]


def get_workspace_repository(
    db: DBSession,
) -> WorkspaceRepository:
    return WorkspaceRepository(db)


WorkspaceRepositoryDep = Annotated[
    WorkspaceRepository,
    Depends(get_workspace_repository),
]


def get_workspace_member_repository(
    db: DBSession,
) -> WorkspaceMemberRepository:
    return WorkspaceMemberRepository(db)


WorkspaceMemberRepositoryDep = Annotated[
    WorkspaceMemberRepository,
    Depends(get_workspace_member_repository),
]


def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    refresh_repository: RefreshTokenRepositoryDep,
) -> UserService:
    return UserService(
        repository,
        refresh_repository,
    )


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]

def get_auth_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    refresh_repository: RefreshTokenRepositoryDep,
) -> AuthService:
    return AuthService(
        repository,
        refresh_repository,
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]

# HTTP Bearer Authentication
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> User:

    # 1. Kiểm tra có gửi Bearer Token không
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Giải mã và xác thực JWT
    try:
        payload = decode_access_token(credentials.credentials)

        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdigit():
            raise ValueError("Invalid user ID in token")

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Tìm User trong database
    user = await repository.get_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Kiểm tra tài khoản có đang hoạt động không
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]


def require_roles(*allowed_roles: str):
    async def role_checker(
        current_user: CurrentUser,
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return role_checker


def get_workspace_service(
    db: DBSession,
    workspace_repository: WorkspaceRepositoryDep,
    member_repository: WorkspaceMemberRepositoryDep,
    user_repository: UserRepositoryDep,
) -> WorkspaceService:
    return WorkspaceService(
        session=db,
        workspace_repository=workspace_repository,
        member_repository=member_repository,
        user_repository=user_repository,
    )


WorkspaceServiceDep = Annotated[
    WorkspaceService,
    Depends(get_workspace_service),
]