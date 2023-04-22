import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEATHER_TOKEN = os.environ.get("WEATHER_TOKEN")
CURRENCY_TOKEN = os.environ.get("CURRENCY_TOKEN")

bot = Bot(token=BOT_TOKEN)
