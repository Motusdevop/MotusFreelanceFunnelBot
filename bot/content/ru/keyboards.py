from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class MenuInlineKeyboard:
    keyboard = [
        [InlineKeyboardButton(text="Заказать разработку", callback_data="development")],
        [InlineKeyboardButton(text="Записаться на обучение", callback_data="training")],
        [InlineKeyboardButton(text="Обо мне", callback_data="about")],
        [
            InlineKeyboardButton(text="Отзывы", callback_data="reviews"),
            InlineKeyboardButton(text="Оставить отзыв", callback_data="feedback"),
        ],
        [InlineKeyboardButton(text="Связаться со мной", callback_data="contact")],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


class BackToMenuInlineKeyboard:
    keyboard = [[InlineKeyboardButton(text="Назад в меню", callback_data="menu")]]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


class FormInlineKeyboard:

    def __init__(self, form_button_text: str, form_url: str):
        self.keyboard = [
            [
                InlineKeyboardButton(
                    text=form_button_text, url=form_url, callback_data="form"
                )
            ],
            [InlineKeyboardButton(text="Назад в меню", callback_data="menu")],
        ]

        self.markup = InlineKeyboardMarkup(inline_keyboard=self.keyboard)
