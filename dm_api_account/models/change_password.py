from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    token: UUID = Field(..., description="Password reset token")
    old_password: str = Field(..., serialization_alias='oldPassword')
    new_password: str = Field(..., serialization_alias='newPassword')
