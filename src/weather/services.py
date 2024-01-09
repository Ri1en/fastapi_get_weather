import re

import requests

from weather.config import Config
from weather.schemas import WeatherModel
from weather.exceptions import ValidError


def get_weather_from_api(
         city: str, config: Config) -> WeatherModel | None:
    if is_valid_city(city):
        url = config.city_url
        res = requests.get(url.format(city=city, api_key=config.api_key))
        data: dict = res.json()
        model_object = WeatherModel.model_construct(**data, **data['main'])
        model_object.weather_description = model_object.weather[0]["description"]
        model_object.kelvin_to_celsius_validate()
        return model_object
    return None


def is_valid_city(city) -> bool:
    if not re.fullmatch(r"^[A-Za-zА-Яа-я\s-]+$", city):
        raise ValidError("City name is invalid")
    return True

