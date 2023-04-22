import aiohttp
from aiohttp import ContentTypeError

from config import CURRENCY_TOKEN

popular_currencies = {
    "Рубль": "RUB",
    "Доллар": "USD",
    "Иена": "JPY",
    "Евро": "EUR",
    "Юань": "CNY"
}


async def get_currency(from_cur: str, to_cur: str, amount: int) -> float:
    """ Sending a request to the API to get the exchange rate """
    to_cur = popular_currencies.get(to_cur.title(), to_cur)             # Conversion of Russian words
    from_cur = popular_currencies.get(from_cur.title(), from_cur)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://api.apilayer.com/exchangerates_data/convert?to={to_cur}&from={from_cur}&amount={amount}',
                    headers={'apikey': CURRENCY_TOKEN}
            ) as resp:
                response = await resp.json()
                return response.get('result')
    except ContentTypeError:                                            # The server is unavailable
        return False



