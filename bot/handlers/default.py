import asyncio
import logging
import pprint

from aiogram import Router, F, html, flags
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods import SendChatAction

log = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Hello World, {hbold(message.from_user.full_name)}!")
    await message.answer("new one")


@router.message(Command("help"))
@router.message(F.text.casefold() == "help")
@flags.chat_action("typing")
async def help_handler(message: Message):
    await message.answer("help")


@router.message(F.text.casefold() == "1")
@flags.chat_action("typing")
async def echo_all(message: Message):
    log.warning(message.chat.id)
    log.warning(pprint.pformat(message.model_dump()))
    await asyncio.sleep(3)
    # log.warning()
    await message.answer(f"<a href=\"https://pyrogram.org/\">URL</a>!", parse_mode=ParseMode.HTML)


@router.message(Command("test"))
async def echo_all(message: Message):
    await message.answer("календарь")
