from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_bot: bool = False
    timezone: Optional[str] = None

    @classmethod
    def from_aiogram(cls, user_obj, timezone: Optional[str] = None) -> "User":
        return cls(
            id=user_obj.id,
            username=user_obj.username,
            first_name=user_obj.first_name,
            last_name=user_obj.last_name,
            language_code=user_obj.language_code,
            is_bot=user_obj.is_bot,
            timezone=timezone,
        )