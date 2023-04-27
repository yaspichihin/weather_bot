import requests

from app.config import settings
from app.yandex.geocode_api import Coords, get_city_coord


def get_weather(city: str) -> dict:
    # Определим координаты города
    coordinates: Coords | None = get_city_coord(city)
    # Если координаты получены вернем данные о погоде иначе None
    if coordinates:
        payload = {'lat': coordinates.lat, 'lon': coordinates.lon, 'lang': 'ru_RU'}
        answer = requests.get(
            'https://api.weather.yandex.ru/v2/forecast',
            params=payload,
            headers=settings.weather_yandex_key
        ).json()
        return answer
