from fastapi.routing import APIRouter
from fastapi import WebSocket

from functools import lru_cache
from typing import Any

from weather.services import WeatherServices
from config import Config


router = APIRouter(
    prefix="/get_weather",
    tags=["weather"]
)


@lru_cache()
def get_settings():
    config = Config()
    return config


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        config: Config = get_settings()
        weather = WeatherServices(config, city=data)
        response: dict[str, Any] = weather.fetch_weather().model_dump()
        await websocket.send_json(response)
