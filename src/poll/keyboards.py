from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_kb_status_poll():
    """ Keyboard transition state between adding response options and other settings """

    kb_poll = ReplyKeyboardBuilder()
    kb_poll.add(KeyboardButton(text="Ввести ещё один вариант ответа")) \
           .add(KeyboardButton(text="Продолжить создавать опрос")) \
           .add(KeyboardButton(text="Отменить всё"))
    kb_poll.adjust(1)
    return kb_poll.as_markup(resize_keyboard=True)


def get_kb_other_options():
    """ Anonymity keyboard and multiple response options """

    kb_poll = ReplyKeyboardBuilder()
    kb_poll.add(KeyboardButton(text="Да")) \
           .add(KeyboardButton(text="Нет"))
    kb_poll.adjust(2)
    return kb_poll.as_markup(resize_keyboard=True)

