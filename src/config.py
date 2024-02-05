import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8')

    api_key: str = Field('api_key', env='.env', alias='API_KEY')
    city_url: str = Field('api.openweathermap.org', env='.env', alias='CITY_URL')
    host: str = Field('hostname', env='.env', alias='MONGO_HOST')
    user: str = Field('user', env='.env', alias='MONGO_INITDB_ROOT_USERNAME')
    db_name: str = Field('db_name', env='.env', alias='MONGO_INITDB_ROOT_DB')
    password: str = Field('password', env='.env', alias='MONGO_INITDB_ROOT_PASSWORD')
    port: str = Field('27018', env='.env', alias='MONGO_PORT')
    me_username: str = Field('username', env='.env', alias='ME_CONFIG_MONGODB_ADMINUSERNAME')
    me_password: str = Field('pass', env='.env', alias='ME_CONFIG_MONGODB_ADMINPASSWORD')
    me_url: str = Field('url', env='.env', alias='ME_CONFIG_MONGODB_URL')
    me_db: str = Field('db_name', env='.env', alias='ME_CONFIG_MONGODB_AUTH_DATABASE')


settings = Config(_env_file=DOTENV)

print(settings.api_key)

