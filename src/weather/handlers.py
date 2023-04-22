from datetime import datetime
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_action import ChatAction

from config import bot
from .states import Weather
from .utils import request_get_weather

router = Router()


@router.message(F.text.in_({'Погода \U000026C5'}))
async def get_city(msg: Message, state: FSMContext):
    await msg.answer("Введите название города")
    await state.set_state(Weather.city)


@router.message(
    Weather.city,
    F.text.regexp(r"[\w]+")
)
async def get_weather(msg: Message, state: FSMContext):
    try:
        response = await request_get_weather(msg.text)                              # Request processing
        if response:
            temp = round(response.get('main').get('temp'))
            humidity = response.get('main').get('humidity')
            pressure = round(response.get('main').get('pressure') / 1.333)
            sunrise = datetime.fromtimestamp(response.get('sys').get('sunrise'))
            sunset = datetime.fromtimestamp(response.get('sys').get('sunset'))
            wind = round(response.get('wind').get('speed'), 1)
            general = response.get('general')

            await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)              # Visibility of the bot
            await msg.answer(f"Город: {msg.text}\n"
                             f"Температура: {temp}, {general}\n"
                             f"Влажность: {humidity} %\n"
                             f"Давление: {pressure} мм.рт.столба\n"
                             f"Рассвет и закат: {sunrise.time()} / {sunset.time()}\n"
                             f"Продолжительность дня: {sunset - sunrise}\n"
                             f"Скорость ветра: {wind} м/с"
                             )
            await state.clear()
        else:                                                                        # The server is unavailable
            await msg.answer("В данный момент сервис прогноза погоды притерпел сбои в системе.\n"
                             "Пожалуйста, попробуйте позже.\n"
                             "Приносим свои извинения!"
                             )
    except TypeError:                                                                # Wrong name of the city
        await msg.answer("Город введен некорректно. Повторите снова.")
