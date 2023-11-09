from os import getenv

from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.enums import ParseMode

from bot.handlers import func, start

router = Router(name=__name__)


async def create_app():
    bot = Bot(getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_routers(router)

    dp.include_routers(*[
        func.router,
        start.router,
    ])

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
