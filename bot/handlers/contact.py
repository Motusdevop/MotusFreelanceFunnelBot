from aiogram import Router
from aiogram.types import CallbackQuery
from loguru import logger

from content.ru.texts import contact_text
from content.ru.keyboards import BackToMenuInlineKeyboard

router = Router()


@router.callback_query(lambda c: c.data == "contact")
async def show_contact(callback_query: CallbackQuery):
    """
    Show contact information.
    """
    logger.info(f"Contact button from {callback_query.from_user.id}")
    await callback_query.message.edit_text(text=contact_text)
    await callback_query.message.edit_reply_markup(reply_markup=BackToMenuInlineKeyboard())