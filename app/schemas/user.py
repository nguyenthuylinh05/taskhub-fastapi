from pydantic import BaseModel, Field, field_validator


class UserUpdate(BaseModel):
    full_name: str = Field(
        min_length=1,
        max_length=150,
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Full name cannot be empty")

        return value


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)