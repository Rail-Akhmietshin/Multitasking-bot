import asyncio
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_action import ChatAction

from config import bot
from .states import Currency
from .utils import get_currency

router = Router()


@router.message(F.text.in_({'Валюта \U0001F4B1'}))
async def to_currency(msg: Message, state: FSMContext):
    await msg.answer("Из какой валюты?")
    await state.set_state(Currency.FROM)


@router.message(
    Currency.FROM,
    F.text.regexp(r"[\w]+")
)
async def amount(msg: Message, state: FSMContext):
    await state.update_data(from_cur=msg.text)
    await msg.answer("Какую сумму?")
    await state.set_state(Currency.AMOUNT)


@router.message(
    Currency.AMOUNT,
    F.text.regexp(r"[\d]+")
)
async def from_currency(msg: Message, state: FSMContext):
    await state.update_data(amount=msg.text)
    await msg.answer("В какую валюту?")
    await state.set_state(Currency.TO)


@router.message(
    Currency.TO,
    F.text.regexp(r"[\w]+")
)
async def amount(msg: Message, state: FSMContext):
    await state.update_data(to_cur=msg.text)
    data = await state.get_data()
    to_cur, from_cur = data.get("to_cur"), data.get("from_cur")
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)                  # Visibility of the bot
    result = await get_currency(from_cur, to_cur, data.get("amount"))           # Request processing
    if result:
        await msg.answer(f"{from_cur} -> {to_cur} = {round(result, 2)} {to_cur.lower()} ")
    else:
        await msg.answer("В данный момент сервис обмена валют притерпел сбои в системе.\n"
                         "Пожалуйста, попробуйте позже.\n"
                         "Приносим свои извинения!"
                         )
    await state.clear()
