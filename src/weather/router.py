from fastapi.routing import APIRouter
from fastapi import WebSocket, Depends

from functools import lru_cache

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
async def websocket_endpoint(websocket: WebSocket, config: Config = Depends(get_settings)):
    await websocket.accept()
    while True:
        data: str = await websocket.receive_text()
        weather = WeatherServices(config, city=data)
        response: dict = weather.fetch_weather()
        await websocket.send_json(response)
