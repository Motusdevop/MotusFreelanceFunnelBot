import asyncio
from aiogram import Bot, Dispatcher

from config import settings, default_bot_properties, logging

from handlers.base import router as commands_router

TOKEN = settings.token.get_secret_value()

bot = Bot(token=TOKEN, default=default_bot_properties)


async def main():
    dp = Dispatcher()
    dp.include_router(commands_router)
    logging.info('Bot started')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
