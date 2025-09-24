from aiogram import Router
from aiogram.types import CallbackQuery
from loguru import logger

from content.ru.texts import feedback_text
from content.ru.keyboards import FormInlineKeyboard
from config import settings

router = Router()


@router.callback_query(lambda c: c.data == "feedback")
async def feedback_request(callback_query: CallbackQuery):
    """
    Show feedback form.
    """
    logger.info(f"Feedback button from {callback_query.from_user.id}")
    keyboard = FormInlineKeyboard(
        form_button_text="Оставить отзыв",
        form_url=settings.FEEDBACK_FORM_URL,
    )
    await callback_query.message.edit_text(text=feedback_text)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
