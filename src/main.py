from fastapi import FastAPI
from dotenv import load_dotenv

from pages.router import router as router_page
from weather.router import router as router_weather

load_dotenv('../.env')


app = FastAPI(title="get_weather")

app.include_router(router_page)
app.include_router(router_weather)
