from aiogram import Router
from aiogram.filters import CommandStart

from weather import fetch_weather

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message):
    await message.reply('Введите город')


@router.message()
async def message(message):
    city = message.text.strip()
    try:
        weather_info = await fetch_weather(city)
        await message.answer(weather_info)
    except Exception:
        await message.reply(f'Такого города не существует')
