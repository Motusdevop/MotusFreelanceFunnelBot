from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from datetime import datetime
from zoneinfo import ZoneInfo
from loguru import logger

import models
from repository import USERS_TABLE
from utils.funnel import send_message_to_admins


class ActivityLoggerMiddleware(BaseMiddleware):
    """
    Middleware that logs and stores user activity
    for both messages and callbacks.
    """

    async def __call__(self, handler, event, data):
        result = await handler(event, data)

        user_id = event.from_user.id
        callback_data = event.data if isinstance(event, CallbackQuery) else None
        command = handler.__name__

        client = models.User(
            chat_id=user_id,
            first_name=event.from_user.first_name,
            last_name=event.from_user.last_name,
            username=(
                "@" + event.from_user.username if event.from_user.username else None
            ),
            last_activity=datetime.now(ZoneInfo("Europe/Moscow")),
            command=command,
            callback_data=callback_data,
        )

        await USERS_TABLE.append(client)
        logger.info(
            f"User {client.chat_id} activity saved: command={command}, callback={callback_data}"
        )

        if (
            callback_data
            and callback_data not in ("menu", "about")
            and not callback_data.startswith("review:")
        ):
            text = (
                "User activity:\n\n"
                f"first_name: {client.first_name}\nlast_name: {client.last_name}\n"
                f"chat_id: {client.chat_id}\nusername: {client.username}\n\n"
                f"clicked button: {callback_data}"
            )
            await send_message_to_admins(event.bot, text)

        return result
