from typing import Any, Dict, Optional, Union

from aiogram.filters import Filter
from aiogram.types import Message, User


class HelloFilter(Filter):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    async def __call__(
        self,
        message: Message,
        event_from_user: User
    ) -> Union[bool, Dict[str, Any]]:
        if message.text.casefold() == "hello":
            return {"name": event_from_user.mention_html(name=self.name)}
        return False
