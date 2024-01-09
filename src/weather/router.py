from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect, Depends
from weather.services import get_weather_from_api
from weather.config import Config

from functools import lru_cache


router = APIRouter(
    prefix="/get_weather",
    tags=["weather"]
)


@lru_cache()
def get_settings():
    config = Config()
    return config


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, config: Config = Depends(get_settings)):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        weather = get_weather_from_api(data, config)
        weather_message = f"""
                    Weather in {weather.city}:\n
                    average temperature : {weather.temp}\n
                    minimal temperature : {weather.temp_min}\n
                    maximum temperature : {weather.temp_max}\n
                    humidity: {weather.humidity}\n
                    weather description: {weather.weather_description}
                    """
        await websocket.send_text(weather_message)


@router.get("/vars")
async def env(config: Config = Depends(get_settings)):
    return {
        "api_key": config.api_key,
        "url": config.city_url
    }
