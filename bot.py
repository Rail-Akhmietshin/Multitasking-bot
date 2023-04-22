import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config import bot
from src.main.handlers import router as menu_router
from src.weather.handlers import router as weather_router
from src.currency.handlers import router as currency_router
from src.poll.handlers import router as poll_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    redis = Redis(host="localhost")

    dp = Dispatcher(storage=RedisStorage(redis=redis))

    dp.include_router(menu_router)\
      .include_router(weather_router)\
      .include_router(currency_router)\
      .include_router(poll_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())