from aiogram import Router
from aiogram.types import CallbackQuery
from loguru import logger

from content.ru.texts import training_text
from content.ru.keyboards import FormInlineKeyboard
from config import settings

router = Router()


@router.callback_query(lambda c: c.data == "training")
async def training_request(callback_query: CallbackQuery):
    """
    Show training request form.
    """
    logger.info(f"Training button from {callback_query.from_user.id}")
    keyboard = FormInlineKeyboard(
        form_button_text="Оставить заявку на обучение",
        form_url=settings.TRAINING_FORM_URL,
    )
    await callback_query.message.edit_text(text=training_text)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
