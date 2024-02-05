import requests
from datetime import datetime

from config import settings, Config
from weather.schemas import WeatherModel, WeatherResponseModel
from db.database import MongoDb
from weather.validators import is_valid_city


class WeatherServices:
    def __init__(self, config, city):
        self.config: Config = config
        self.city: str = city

    def get_weather_from_api(self) -> dict | None:
        if is_valid_city(self.city):
            url = self.config.city_url
            res = requests.get(url.format(city=self.city, api_key=self.config.api_key))
            data: dict = res.json()
            model_object = WeatherModel.model_construct(**data, **data['main'])
            model_object.weather_description = model_object.weather[0]["description"]
            model_object.kelvin_to_celsius_validate()
            return model_object.model_dump()
        return None

    def get_weather_from_db(self) -> dict | None:
        formats: str = "%Y-%m-%d"
        today: str = datetime.now().strftime(formats)
        query: dict = {
            "city": self.city,
            "response_time": today
        }
        with MongoDb(self.config, 'test') as collection:
            result = collection.find_one(query)
        if result:
            return WeatherResponseModel.model_construct(**result).model_dump()
        return None

    def fetch_weather(self) -> dict | None:
        if self.get_weather_from_db():
            return self.get_weather_from_db()
        else:
            data: dict = self.get_weather_from_api()
            if data:
                response_data: dict = self.save_weather_in_db(data)
                return response_data
            else:
                return None

    @staticmethod
    def save_weather_in_db(data: dict) -> dict:
        formats: str = "%Y-%m-%d"
        today: str = datetime.now().strftime(formats)
        data['response_time'] = today
        serialized_data = WeatherResponseModel.model_construct(**data).model_dump()
        with MongoDb(settings, collection='test') as collection:
            collection.insert_one(serialized_data)
        serialized_data.pop('_id')
        return serialized_data
