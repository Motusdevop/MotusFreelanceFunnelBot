import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import models
from config import settings

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)

from content.ru.texts import (
    start_text,
    develompent_text,
    training_text,
    about_text,
    feedback_text,
    contact_text,
)
from content.ru.keyboards import (
    MenuInlineKeyboard,
    BackToMenuInlineKeyboard,
    FormInlineKeyboard,
)

from utils.funnel import send_message_to_admins

from utils.repository import UserTable

router = Router()


def statistics_and_notification(func):
    async def wrapper(*args, **kwargs):
        res = await func(*args)
        handled_entity = args[0]
        callback_data = handled_entity.data if isinstance(handled_entity, CallbackQuery) else None
        client = models.User(
            chat_id=handled_entity.from_user.id,
            first_name=handled_entity.from_user.first_name,
            last_name=handled_entity.from_user.last_name,
            username=(
                "@" + handled_entity.from_user.username if handled_entity.from_user.username else None
            ),
            last_activity=datetime.now(ZoneInfo("Europe/Moscow")),
            command=func.__name__,
            callback_data=callback_data
        )
        await UserTable.append(client)

        if callback_data and callback_data not in ('menu', 'about'):
            text = "Аквтивность:\n\n"
            text += f"first_name: {client.first_name}\nlast_name: {client.last_name}\n"
            text += f"chat_id: {client.chat_id}\n username: {client.username}\n\n"
            text += f"click to button: callback_data: {callback_data}"

            await send_message_to_admins(handled_entity.bot, text)

        return res

    return wrapper


@router.message(CommandStart())
@statistics_and_notification
async def start(message: Message):
    logging.info("command start")

    await message.answer(text=start_text, reply_markup=MenuInlineKeyboard.markup)


@router.callback_query()
@statistics_and_notification
async def button_callback(callback_query: CallbackQuery):
    match callback_query.data:
        case "menu":
            logging.info("button click menu")
            await callback_query.message.edit_text(text=start_text)
            await callback_query.message.edit_reply_markup(
                reply_markup=MenuInlineKeyboard.markup
            )
        case "development":
            logging.info("button click development")

            keyboard = FormInlineKeyboard(
                form_button_text="Оставить заявку на разработку",
                form_url=settings.DEVELOPMENT_FORM_URL,
            )

            await callback_query.message.edit_text(text=develompent_text)
            await callback_query.message.edit_reply_markup(reply_markup=keyboard.markup)
        case "training":
            logging.info("button click training")
            await callback_query.message.edit_text(text=training_text)
            keyboard = FormInlineKeyboard(
                form_button_text="Оставить заявку на обучение",
                form_url=settings.TRAINING_FORM_URL,
            )
            await callback_query.message.edit_reply_markup(reply_markup=keyboard.markup)
        case "about":
            logging.info("button click about")
            await callback_query.message.edit_text(text=about_text)
            await callback_query.message.edit_reply_markup(
                reply_markup=BackToMenuInlineKeyboard.markup
            )
        case "reviews":
            ...
        case "feedback":
            logging.info("button click feedback")
            keyboard = FormInlineKeyboard(
                form_button_text="Оставить отзыв", form_url=settings.FEEDBACK_FORM_URL
            )
            await callback_query.message.edit_text(text=feedback_text)
            await callback_query.message.edit_reply_markup(reply_markup=keyboard.markup)
        case "contact":
            logging.info("button click contact")
            await callback_query.message.edit_text(text=contact_text)
            await callback_query.message.edit_reply_markup(
                reply_markup=BackToMenuInlineKeyboard.markup
            )
