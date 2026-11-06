from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.roles import WorkspaceRole

class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Workspace name cannot be empty")

        return value


class WorkspaceResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkspaceMemberCreate(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    role: WorkspaceRole = WorkspaceRole.VIEWER

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()

        if not value:
            raise ValueError("Email cannot be empty")

        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: WorkspaceRole) -> WorkspaceRole:
        if value == WorkspaceRole.OWNER:
            raise ValueError("Use role update to promote a member to OWNER")
        return value


class WorkspaceMemberRoleUpdate(BaseModel):
    role: WorkspaceRole


class WorkspaceMemberResponse(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: WorkspaceRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)    