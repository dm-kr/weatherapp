import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from routers.weather_router import router as weather_router


async def main():
    dp = Dispatcher()
    dp.include_router(weather_router)

    default = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=default
    )

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
