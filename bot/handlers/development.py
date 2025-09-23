from aiogram import Router
from aiogram.types import CallbackQuery
from loguru import logger

from content.ru.texts import develompent_text
from content.ru.keyboards import FormInlineKeyboard
from config import settings

router = Router()


@router.callback_query(lambda c: c.data == "development")
async def development_request(callback_query: CallbackQuery):
    """
    Show development request form.
    """
    logger.info(f"Development button from {callback_query.from_user.id}")
    keyboard = FormInlineKeyboard(
        form_button_text="Оставить заявку на разработку",
        form_url=settings.DEVELOPMENT_FORM_URL,
    )
    await callback_query.message.edit_text(text=develompent_text)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)