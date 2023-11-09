import asyncio
import logging
import pprint

from aiogram import Router, F, html, flags
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods import SendChatAction

log = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello World, {hbold(message.from_user.full_name)}!")


@router.message()
@flags.chat_action("typing")
async def echo_all(message: Message):
    log.warning(message.chat.id)
    log.warning(pprint.pformat(message.model_dump()))
    await asyncio.sleep(3)
    # log.warning()
    await message.answer(f"<a href=\"https://pyrogram.org/\">URL</a>!", parse_mode=ParseMode.HTML)
