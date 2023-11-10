import asyncio
import logging
import pprint
from typing import Any

from aiogram import Router, F, html, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot.states import Moon
from bot.keyboards import calendar_keyboard

log = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(Command("moon"))
@router.message(F.text.casefold() == "moon")
async def moon_handler(message: Message, state: FSMContext) -> Any:
    await state.set_state(Moon.location)
    return message.answer("Отправьте геопозицию города вашего рождения")


@router.message(Moon.location)
async def datetime_select(message: Message, state: FSMContext) -> Any:
    await state.set_state(Moon.datetime)
    log.warning(pprint.pformat(message.location))
    await state.update_data(name=message.location)

    markup = await calendar_keyboard.create_calendar()
    return message.answer("Выберите дату и время дня рождения:",
                          reply_markup=markup)


@router.callback_query(F.data)
async def inline_handler(callback: CallbackQuery):
    selected, date = await calendar_keyboard.calendar_selection(callback)
    if selected:
        await callback.message.answer(
            text="You selected %s" % (date.strftime("%d/%m/%Y")),
            # reply_markup=ReplyKeyboardRemove()
        )




@router.message(Moon.datetime)
async def datetime_handler(message: Message, state: FSMContext) -> Any:
    await state.set_state(Moon.final)
    log.warning(pprint.pformat(message.model_dump()))
    await state.update_data(name=message.text)
    return message.answer("asd")
