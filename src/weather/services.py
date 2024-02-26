import requests
from datetime import datetime
from typing import Any

from config import settings, Config
from weather.schemas import WeatherModel
from db.database import MongoDb


class WeatherServices:
    def __init__(self, config: Config, city: str):
        self.config = config
        self.city = city

    def get_weather_from_api(self) -> WeatherModel | None:
        url = self.config.city_url
        res = requests.get(url.format(city=self.city, api_key=self.config.api_key))
        data: dict = res.json()
        model_object = WeatherModel.model_construct(**data, **data['main'])
        model_object.weather_description = model_object.weather[0]["description"]
        formats = "%Y-%m-%d"
        today: str = datetime.now().strftime(formats)
        model_object.response_date = today
        model_object.response_time = datetime.now().strftime('%H:%M:%S')
        model_object.kelvin_to_celsius_validate()
        return model_object

    def get_weather_from_db(self) -> WeatherModel | None:
        formats = "%Y-%m-%d"
        today: str = datetime.now().strftime(formats)
        query: dict[str, Any] = {
            "city": self.city,
            "response_date": today
        }
        with MongoDb(self.config, 'test') as collection:
            result = collection.find_one(query)
        if result:
            return WeatherModel.model_construct(**result)
        return None

    def fetch_weather(self) -> WeatherModel | None:
        if self.get_weather_from_db():
            return self.get_weather_from_db()
        else:
            data: WeatherModel = self.get_weather_from_api()
            if data:
                self.save_weather_in_db(data)
                return data
            else:
                return None

    @staticmethod
    def save_weather_in_db(data: WeatherModel):
        serialized_data = data.model_dump()
        with MongoDb(settings, collection='test') as collection:
            collection.insert_one(serialized_data)
