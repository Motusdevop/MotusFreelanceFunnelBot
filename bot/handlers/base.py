import logging
from datetime import datetime

import models
from config import settings

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update, CallbackQuery

from content.ru.texts import start_text, develompent_text, training_text, about_text, feedback_text, contact_text
from content.ru.keyboards import MenuInlineKeyboard, BackToMenuInlineKeyboard, FormInlineKeyboard

from utils import funnel
from utils.google_sheet import GoogleSheet
from utils.storage import UserTable

router = Router()


def client_data_to_str(client_data: dict):
    return 'first_name: {first_name}\nlast_name: {last_name}\nusername: @{username}\ndatetime: {datetime}'.format(
        **client_data)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    logging.info('command start')

    await message.answer(text=start_text, reply_markup=MenuInlineKeyboard.markup)

    client = models.User(
        chat_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username='@' + message.from_user.username,
        last_activity=datetime.now().strftime('%d.%m %H:%M'))

    flag = True

    for user in UserTable.table:
        if user.chat_id == client.chat_id:
            flag = False
            break

    if flag:
        UserTable.append(client)
        logging.info('new user')


@router.callback_query()
async def button_callback(callback_query: CallbackQuery):
    match callback_query.data:
        case 'menu':
            logging.info('button click menu')
            await callback_query.message.edit_text(text=start_text)
            await callback_query.message.edit_reply_markup(reply_markup=MenuInlineKeyboard.markup)
        case 'development':
            logging.info('button click development')

            keyboard = FormInlineKeyboard(form_button_text='Оставить заявку на разработку',
                                          form_url=settings.development_form_url)

            await callback_query.message.edit_text(text=develompent_text)
            await callback_query.message.edit_reply_markup(reply_markup=keyboard.markup)
        case 'training':
            logging.info('button click training')
            await callback_query.message.edit_text(text=training_text)
            keyboard = FormInlineKeyboard(form_button_text='Оставить заявку на обучение',
                                          form_url=settings.training_form_url)
            await callback_query.message.edit_reply_markup(reply_markup=keyboard.markup)
        case 'about':
            logging.info('button click about')
            await callback_query.message.edit_text(text=about_text)
            await callback_query.message.edit_reply_markup(reply_markup=BackToMenuInlineKeyboard.markup)
        case 'reviews':
            reviews_gs = GoogleSheet(settings.credentials_path, settings.sheet_name, settings.REVIEWS_WORKSHEET_INDEX)

            reviews = reviews_gs.read_all_records()

            review = reviews.pop(0)

            text = f"""Последний отзыв:
{review['Имя']} {review['Оценка']}/5:
Услуга: {review['Услуга']}

Отзыв:
{review['Отзыв']}

Дата:
{review['Дата']}"""

            await callback_query.message.edit_text(text=text)
            await callback_query.message.edit_reply_markup(reply_markup=BackToMenuInlineKeyboard.markup)
        case 'reviews_next':
            ...
        case 'reviews_prev':
            ...
        case 'feedback':
            logging.info('button click feedback')
            keyboard = FormInlineKeyboard(form_button_text='Оставить отзыв',
                                          form_url=settings.feedback_form_url)
            await callback_query.message.edit_text(text=feedback_text)
            await callback_query.message.edit_reply_markup(reply_markup=keyboard.markup)
        case 'contact':
            logging.info('button click contact')
            await callback_query.message.edit_text(text=contact_text)
            await callback_query.message.edit_reply_markup(reply_markup=BackToMenuInlineKeyboard.markup)
