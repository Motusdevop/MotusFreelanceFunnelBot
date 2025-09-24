
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class MenuInlineKeyboard(InlineKeyboardMarkup):
    """
    Main menu keyboard.
    """

    def __init__(self, review_avg: float | None = None):
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Заказать разработку", callback_data="development"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Записаться на обучение", callback_data="training"
                )
            ],
            [InlineKeyboardButton(text="Обо мне", callback_data="about")],
            [
                InlineKeyboardButton(
                    text="Отзывы" + f" {round(review_avg, 2)} ⭐" if review_avg else "",
                    callback_data="reviews",
                ),
                InlineKeyboardButton(text="Оставить отзыв", callback_data="feedback"),
            ],
            [InlineKeyboardButton(text="Связаться со мной", callback_data="contact")],
        ]
        super().__init__(inline_keyboard=keyboard)


class BackToMenuInlineKeyboard(InlineKeyboardMarkup):
    """
    Single button to return to menu.
    """

    def __init__(self):
        keyboard = [[InlineKeyboardButton(text="Назад в меню", callback_data="menu")]]
        super().__init__(inline_keyboard=keyboard)


class FormInlineKeyboard(InlineKeyboardMarkup):
    """
    Keyboard with form button and back to menu.
    """

    def __init__(self, form_button_text: str, form_url: str):
        keyboard = [
            [InlineKeyboardButton(text=form_button_text, url=form_url)],
            [InlineKeyboardButton(text="Назад в меню", callback_data="menu")],
        ]
        super().__init__(inline_keyboard=keyboard)


class ReviewInlineKeyboard(InlineKeyboardMarkup):
    """
    Keyboard for navigating through reviews.
    """

    def __init__(self, index: int, total: int):
        keyboard = []
        row = []
        if index > 0:
            row.append(
                InlineKeyboardButton(
                    text="⬅️ Предыдущий", callback_data=f"review:{index - 1}"
                )
            )
        if index < total - 1:
            row.append(
                InlineKeyboardButton(
                    text="Следующий ➡️", callback_data=f"review:{index + 1}"
                )
            )

        if row:
            keyboard.append(row)

        keyboard.append(
            [InlineKeyboardButton(text="Назад в меню", callback_data="menu")]
        )
        super().__init__(inline_keyboard=keyboard)
