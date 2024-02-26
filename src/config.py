import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8')

    api_key: str = Field('api_key', env='.env')
    city_url: str = Field('api.openweathermap.org', env='.env')
    host: str = Field('hostname', env='.env', alias='mongo_host')
    user: str = Field('user', env='.env', alias='mongo_initdb_root_username')
    db_name: str = Field('db_name', env='.env', alias='mongo_initdb_root_db')
    password: str = Field('password', env='.env', alias='mongo_initdb_root_password')
    port: str = Field('27018', env='.env', alias='mongo_port')
    me_username: str = Field('username', env='.env', alias='me_config_mongodb_adminusername')
    me_password: str = Field('pass', env='.env', alias='me_config_mongodb_adminpassword')
    me_url: str = Field('url', env='.env', alias='me_config_mongodb_url')
    me_db: str = Field('db_name', env='.env', alias='me_config_mongodb_auth_database')


settings = Config(_env_file=DOTENV)
