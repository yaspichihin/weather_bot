

def get_weather_answer(
        city: str,
        temp: int,
        feels_like: int,
        wind_speed: int,
        pressure_mm: int
) -> str:
    text: str = (
        f"Погода в {city}\n"
        f"Температура: {temp} C\n"
        f"Ощущается как: {feels_like} C \n"
        f"Скорость ветра: {wind_speed} м/с\n"
        f"Давление: {pressure_mm} мм"
    )
    return text


def get_report_answer(
        city: str,
        temp: int,
        feels_like: int,
        wind_speed: int,
        pressure_mm: int
) -> str:
    text: str = 'Данные по запросу\n' + \
        get_weather_answer(
            city, temp, feels_like,
            wind_speed, pressure_mm
        )
    return text
