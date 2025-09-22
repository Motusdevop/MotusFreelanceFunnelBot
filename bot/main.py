import asyncio
from aiogram import Bot, Dispatcher

import handlers.init
from config import settings, get_default_bot_properties
from handlers import base, development, reviews
from logger_config import setup_logger
from loguru import logger

import handlers
from middlewares.activity_logger import ActivityLoggerMiddleware
from repository import USERS_TABLE, REVIEWS_TABLE

TOKEN = settings.BOT_TOKEN.get_secret_value()
bot = Bot(token=TOKEN, default=get_default_bot_properties())


async def on_startup_callback(dispatcher: Dispatcher) -> None:
    """
    Executed on bot startup.
    Enables periodic sync with Google Sheets.
    """
    logger.info("BOT STARTING...")

    await USERS_TABLE.enable_auto_update()
    await REVIEWS_TABLE.enable_auto_load()

    logger.info("BOT STARTED!")


async def restore_chats_and_notify(bot: Bot) -> None:
    """
    Restore chat IDs from pending updates and notify users
    that the bot is back online.
    """
    updates = await bot.get_updates()
    chats = {update.message.chat.id for update in updates if update.message}

    for chat_id in chats:
        await bot.send_message(
            chat_id=chat_id,
            text="Бот восстановил свою работу! Простите за неудобства!",
        )

    logger.info(f"Restored and notified {len(chats)} chats")


async def main() -> None:
    """
    Entry point of the bot application.
    """
    setup_logger()

    dp = Dispatcher()

    # Middleware
    dp.message.middleware(ActivityLoggerMiddleware())
    dp.callback_query.middleware(ActivityLoggerMiddleware())

    # Routers
    handlers.init.setup_handlers(dp)

    dp.startup.register(on_startup_callback)

    await restore_chats_and_notify(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
