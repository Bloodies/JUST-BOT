from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.handlers import func, default, moon


async def create_app():
    bot = Bot(getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)

    dp = Dispatcher()

    dp.include_routers(*[
        default.router,
        func.router,
        moon.router,
    ])

    await bot.set_my_commands([
        BotCommand(command=c, description=d) for c, d in [
            ("/start", "Перезапуск"),
            ("/help", "Информация о боте"),
            ("/moon", "moon"),
            ("/test", "test")
        ]
    ])

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
