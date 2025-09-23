from aiogram import Router
from aiogram.types import CallbackQuery
from loguru import logger

from repository import REVIEWS_TABLE
from content.ru.keyboards import ReviewInlineKeyboard
from utils.formatter import format_review

router = Router()


@router.callback_query(lambda c: c.data == "reviews")
async def show_reviews(callback_query: CallbackQuery):
    """
    Show first review and navigation buttons.
    """
    reviews = REVIEWS_TABLE.get_reviews()
    if not reviews:
        await callback_query.message.edit_text("Отзывов пока нет 🙃")
        await callback_query.answer()
        return

    logger.info(f"Reviews button from {callback_query.from_user.id}")

    await callback_query.message.edit_text(
        text=format_review(reviews[0]),
        reply_markup=ReviewInlineKeyboard(0, len(reviews)),
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data.startswith("review:"))
async def paginate_reviews(callback_query: CallbackQuery):
    """
    Paginate reviews with next/prev buttons.
    """
    index = int(callback_query.data.split(":")[1])
    reviews = REVIEWS_TABLE.get_reviews()

    if 0 <= index < len(reviews):
        logger.info(f"User {callback_query.from_user.id} viewing review {index + 1}/{len(reviews)}")
        await callback_query.message.edit_text(
            text=format_review(reviews[index]),
            reply_markup=ReviewInlineKeyboard(index, len(reviews)),
            parse_mode="HTML",
        )
    await callback_query.answer()
