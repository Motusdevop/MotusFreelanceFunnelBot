from typing import List

from aiogram import Bot

from config import settings


async def send_message_to_admins(bot: Bot, text: str):
    for admin_id in settings.ADMINS:
        await bot.send_message(chat_id=admin_id, text=text, parse_mode="Markdown", disable_notification=True)