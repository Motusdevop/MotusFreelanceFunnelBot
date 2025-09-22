from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from loguru import logger

from content.ru.texts import start_text, about_text
from content.ru.keyboards import MenuInlineKeyboard, BackToMenuInlineKeyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    """
    Handle /start command.
    """
    logger.info(f"/start from {message.from_user.id}")
    await message.answer(text=start_text, reply_markup=MenuInlineKeyboard())


@router.callback_query(lambda c: c.data == "menu")
async def show_menu(callback_query: CallbackQuery):
    """
    Show main menu.
    """
    logger.info(f"Menu button from {callback_query.from_user.id}")
    await callback_query.message.edit_text(text=start_text)
    await callback_query.message.edit_reply_markup(reply_markup=MenuInlineKeyboard())


@router.callback_query(lambda c: c.data == "about")
async def show_about(callback_query: CallbackQuery):
    """
    Show about section.
    """
    logger.info(f"About button from {callback_query.from_user.id}")
    await callback_query.message.edit_text(text=about_text)
    await callback_query.message.edit_reply_markup(reply_markup=BackToMenuInlineKeyboard())
