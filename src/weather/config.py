from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding='utf-8')

    api_key: str = Field('api_key', env='.env', alias='API_KEY')
    city_url: str = Field('api.openweathermap.org', env='.env', alias='CITY_URL')


config = Config(_env_file='../.env')


print(config.api_key)

