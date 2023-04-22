from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_kb_menu_keyboard():
    """ Menu keyboard """

    kb_menu = ReplyKeyboardBuilder()
    kb_menu.add(KeyboardButton(text="Погода \U000026C5")) \
        .add(KeyboardButton(text="Валюта \U0001F4B1")) \
        .add(KeyboardButton(text="Милое животное \U0001F43E")) \
        .add(KeyboardButton(text="Создать опрос \U0001F5EF"))
    kb_menu.adjust(2)
    return kb_menu.as_markup(resize_keyboard=True)


