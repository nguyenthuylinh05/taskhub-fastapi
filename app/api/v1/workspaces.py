from fastapi import APIRouter, Response, status

from app.api.dependencies import CurrentUser, WorkspaceServiceDep
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
    WorkspaceMemberRoleUpdate,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    workspace_data: WorkspaceCreate,
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
):
    """Create a workspace. The creator becomes its owner."""
    return await service.create_workspace(
        name=workspace_data.name,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
async def list_my_workspaces(
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
):
    """List workspaces where the current user is a member."""
    return await service.list_my_workspaces(current_user=current_user)


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
async def get_workspace(
    workspace_id: int,
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
):
    """Get a workspace accessible to the current user."""
    return await service.get_workspace(
        workspace_id=workspace_id,
        current_user=current_user,
    )


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_workspace(
    workspace_id: int,
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
) -> Response:
    """Delete a workspace. Only its owner or a global admin can do this."""
    await service.delete_workspace(
        workspace_id=workspace_id,
        current_user=current_user,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get(
    "/{workspace_id}/members",
    response_model=list[WorkspaceMemberResponse],
)
async def list_workspace_members(
    workspace_id: int,
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
):
    return await service.list_members(
        workspace_id=workspace_id,
        current_user=current_user,
    )


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_workspace_member(
    workspace_id: int,
    member_data: WorkspaceMemberCreate,
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
):
    return await service.add_member(
        workspace_id=workspace_id,
        email=member_data.email,
        role=member_data.role,
        current_user=current_user,
    )


@router.patch(
    "/{workspace_id}/members/{user_id}",
    response_model=WorkspaceMemberResponse,
)
async def update_workspace_member_role(
    workspace_id: int,
    user_id: int,
    role_data: WorkspaceMemberRoleUpdate,
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
):
    return await service.update_member_role(
        workspace_id=workspace_id,
        user_id=user_id,
        new_role=role_data.role,
        current_user=current_user,
    )


@router.delete(
    "/{workspace_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_workspace_member(
    workspace_id: int,
    user_id: int,
    current_user: CurrentUser,
    service: WorkspaceServiceDep,
) -> Response:
    await service.remove_member(
        workspace_id=workspace_id,
        user_id=user_id,
        current_user=current_user,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)