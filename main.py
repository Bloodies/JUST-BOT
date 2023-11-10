import asyncio
import logging

from dotenv import load_dotenv

from bot.app import create_app


log = logging.getLogger(__name__)
FORMAT = '%(asctime)s | %(name)s | %(levelname)s | [%(filename)s::%(lineno)d] || %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

load_dotenv()


if __name__ == "__main__":
    log.info('BOT startup')
    asyncio.run(create_app())
