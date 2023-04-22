from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.filters.command import Command
from aiogram.types import Message

from config import bot
from .keyboards import get_kb_menu_keyboard
from .utils import get_url_photo

router = Router()


@router.message(Command(commands=['start']))
@router.message(F.text == "Мы переместились в меню!")
async def menu(msg: Message):
    await msg.answer("Привет! Вот что я умею:", reply_markup=get_kb_menu_keyboard())


@router.message(F.text == "Милое животное \U0001F43E")
async def get_animal(msg: Message):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)                          # Visibility of the bot
    url = await get_url_photo()                                                         # Request processing
    await bot.send_photo(msg.chat.id, photo=url)



