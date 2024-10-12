from apiclient import APIClient, Resource
from config import settings
from redis_client import RedisClient


def render_weather(city, data):
    wind_dirs = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    temp_c = data.get('temp_c')
    feelslike_c = data.get('feelslike_c')
    condition = data.get('condition').get('text')
    humidity = data.get('humidity')
    wind_kph = data.get('wind_kph')
    wind_dir_index = data.get('wind_degree') // 45
    gust_kph = data.get('gust_kph')
    return (
        f'*Погода в городе {city}:*\n\n'
        f'*Температура:* {temp_c}°C\n'
        f'*Ощущается как:* {feelslike_c}°C\n'
        f'*Влажность:* {humidity}%\n'
        f'*Описание:* {condition}\n'
        f'*Ветер:* {wind_dirs[wind_dir_index]} - {wind_kph / 3.6:.2f} м/с\n'
        f'*Порывы до:* {gust_kph / 3.6:.2f} м/с'
    )


async def fetch_weather(city):
    api_url = 'https://api.weatherapi.com/v1/'
    api_key = settings.WEATHER_API_KEY
    async with APIClient(base_url=api_url, api_key=api_key) as client:
        current_weather = Resource(client, resource_path='current.json')
        params = {
            'key': api_key,
            'q': city,
            'lang': 'ru'
        }
        key = f'weatherapp:{city}'
        async with RedisClient() as redis:
            data = await redis.get(key)
            if data:
                return render_weather(city, data)
            data = await current_weather.get(params=params)
            data = data.get('current', None)
            if not data:
                raise Exception
            await redis.set(key, data)
        return render_weather(city, data)
