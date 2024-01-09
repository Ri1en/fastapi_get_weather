from pydantic import BaseModel, Field


class WeatherModel(BaseModel):
    city: str = Field(pattern=r'^[A-Za-zА-Яа-я\s-]+$', alias='name')
    coord: dict
    temp: float
    temp_min: float
    temp_max: float
    humidity: float
    weather: list[dict]
    weather_description: str = Field(init_var=True)

    def kelvin_to_celsius_validate(self) -> None:
        self.temp = float('{:.3f}'.format(self.temp - 273))
        self.temp_max = float('{:.3f}'.format(self.temp_max - 273))
        self.temp_min = float('{:.3f}'.format(self.temp_min - 273))
