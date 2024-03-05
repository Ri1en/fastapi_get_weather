from pydantic import BaseModel, Field
from typing import Any


class WeatherModel(BaseModel):
    city: str = Field(pattern=r'^[A-Za-zА-Яа-я\s-]+$', alias='name')
    temp: float
    humidity: float
    weather: list[dict] = Field(exclude=True)
    weather_description: str = Field(init_var=True)
    response_date: str = Field(init_var=True)
    response_time: str = Field(init_var=True)

    def kelvin_to_celsius_validate(self) -> None:
        self.temp = float('{:.3f}'.format(self.temp - 273))
