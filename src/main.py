from fastapi import FastAPI

from pages.router import router as router_page
from weather.router import router as router_weather


app = FastAPI(title="get_weather")

app.include_router(router_page)
app.include_router(router_weather)
