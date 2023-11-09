import logging
from typing import Any

from aiogram import Router
from aiogram.types import Message

from bot.filters.filters import HelloFilter

log = logging.getLogger(__name__)
router = Router(name=__name__)


# @router.message(HelloFilter())
# async def my_handler(message: Message, name: str) -> Any:
#     return message.answer("Hello, {name}!".format(name=name))
