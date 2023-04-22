from random import randint as randomizer

import aiohttp
from bs4 import BeautifulSoup


async def get_url_photo():
    """ Request for a random cute animal """

    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://yandex.co.il/images/search?text=Самые%20Милые%20Животные&nl=1&source=morda'
        ) as resp:
            response = await resp.read()
            soup = BeautifulSoup(response, "lxml")
            match = soup.find_all("img", class_="serp-item__thumb justifier__thumb")
            url = "https:" + match[randomizer(0, len(match) - 1)].get("src")
            return url
