from fastapi import FastAPI
from services.apparel_recommendations.main import get_apparel_recommendations
from services.sunrise_sunset.main import get_sunrise_sunset_today_times_short


app = FastAPI()


@app.get("/sunset_sunrise_today/")
async def sunset_sunrise(latitude: float, longitude: float):
    return get_sunrise_sunset_today_times_short(latitude=latitude, longitude=longitude)


@app.get("/apparel_recommendations_now/")
async def apparel_recommendations(latitude: float, longitude: float):
    return get_apparel_recommendations(latitude=latitude, longitude=longitude)
