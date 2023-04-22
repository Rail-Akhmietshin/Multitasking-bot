from aiohttp import ContentTypeError

from config import WEATHER_TOKEN

import aiohttp

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}


async def request_get_weather(city: str) -> dict | bool:
    """ Sending a request to the API to get a weather forecast """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}&units=metric'
            ) as resp:
                response = await resp.json()
                main = response.get("weather")[0].get('main')
                general = code_to_smile.get(main)                           # Conversion of foreign words into Russian
                response["general"] = general if general else 'Странная сегодня погодка! Советую выглянуть в окно'
                return response
    except ContentTypeError:                                                # The server is unavailable
        return False
