from typing import TypedDict
from uuid import UUID

from app.domain.enums.user_type import UserRole


class UserQueryModel(TypedDict):
    id_: UUID
    username: str
    role: UserRole
    is_active: bool
