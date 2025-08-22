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
    updates = await bot.get_updates()

    chats = list()
    if updates:
        for update in updates:
            if update.message:
                if update.message.chat.id not in chats:
                    chats.append(update.message.chat.id)

    for chat in chats:
        await bot.send_message(text='Бот восстановил свою работу! Простите за неудобства!', chat_id=chat)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
