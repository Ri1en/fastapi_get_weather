from fastapi.routing import APIRouter
from fastapi import WebSocket, Depends
from weather.services import get_weather_from_api
from weather.config import Config
from datetime import datetime

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
        response_time = datetime.now()
        formats = "%Y-%m-%d %H:%M:%S"
        data = {
            "city": weather.city,
            "temp": weather.temp,
            "humidity": weather.humidity,
            "weather_description": weather.weather_description,
            "response_time": response_time.strftime(formats)
        }
        await websocket.send_json(data)

