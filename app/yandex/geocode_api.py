from collections import namedtuple

import requests

from app.config import settings

Coords = namedtuple('Coords', ['lon', 'lat'])


def get_city_name(city: str) -> str:
    payload = {
        'geocode': city,
        'apikey': settings.geocoder_yandex_key,
        'format': 'json'
    }
    answer = requests.get(
        'https://geocode-maps.yandex.ru/1.x',
        params=payload
    ).json()
    is_found: str = (
        answer['response']['GeoObjectCollection']['metaDataProperty']
        ['GeocoderResponseMetaData']['found']
    )
    # Если город определен вернуть его имя, иначе None
    if is_found:
        city_name_geocode: str = (
            answer['response']['GeoObjectCollection']['featureMember'][0]
            ['GeoObject']['name']
        )
        return city_name_geocode


def get_city_coord(city: str) -> Coords | None:
    payload = {
        'geocode': city,
        'apikey': settings.geocoder_yandex_key,
        'format': 'json'
    }
    answer = requests.get(
        'https://geocode-maps.yandex.ru/1.x',
        params=payload
    ).json()
    # Выполняем проверку распознавания города
    is_found: int = int(
        answer['response']['GeoObjectCollection']['metaDataProperty']
        ['GeocoderResponseMetaData']['found']
    )
    # Если город определен вернем координаты иначе None
    if is_found > 0:
        coords = Coords(*answer['response']['GeoObjectCollection']
            ['featureMember'][0]['GeoObject']['Point']['pos'].split())
        return coords
