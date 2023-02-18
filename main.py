from datetime import datetime, timedelta
from enum import Enum

from dateutil import tz
from fastapi import FastAPI
from pydantic import BaseModel

from external_apis.sunrise_sunset.client import get_sunrise_sunset_times
from external_apis.weather.client import get_hourly_weather


class Range(BaseModel):
    min: int
    max: int


class TemperatureLevel(Enum):
    # min max values in Fahrenheit
    VERY_COLD = Range(min=-100, max=25)
    COLD = Range(min=25, max=45)
    COOL = Range(min=45, max=57)
    WARM = Range(min=57, max=67)
    HOT = Range(min=67, max=100)


class WindSpeed(Enum):
    # min max values in miles per hour (mph)
    HIGH = Range(min=10, max=100)
    MEDIUM = Range(min=5, max=10)
    LOW = Range(min=0, max=5)


def _determine_level(weather_metric: Enum, value: int):
    """Determine level of weather metric like wind speed of high, medium or low.
    Args:
        weather_metric: instance of an enum for a weather metric like wind speed or temperature
        value: integer to quantify weather metric rate like wind speed of 8 mph
    Returns:
        weather_metric: enum member
    """
    for member in weather_metric:
        if member.value.min <= value < member.value.max:
            return member


app = FastAPI()


@app.get("/weather_recs/")
async def get_sunrise_sunset_and_clothing_recs(latitude: float, longitude: float):
    # Get weather metrics
    weather_details = get_hourly_weather(latitude=latitude, longitude=longitude)

    apparent_temp_value_now = weather_details.properties.apparent_temperature.now_time_period_value()
    wind_speed_value_now = weather_details.properties.wind_speed.now_time_period_value()
    probability_of_precipitation_value_now = weather_details.properties.probability_of_precipitation.now_time_period_value()
    quantitative_precipitation_value_now = weather_details.properties.quantitative_precipitation.now_time_period_value()
    sky_cover_value_now = weather_details.properties.sky_cover.now_time_period_value()

    # Get sunrise and sunset data
    sunrise_sunset_today_response = get_sunrise_sunset_times(latitude=latitude, longitude=longitude)
    sunrise_time_utc = sunrise_sunset_today_response.results.sunrise_time_utc
    sunset_time_utc = sunrise_sunset_today_response.results.sunset_time_utc

    sunset_time_short = sunset_time_utc.strftime("%Y-%m-%d %H:%M")
    sunrise_time_short = sunrise_time_utc.strftime("%Y-%m-%d %H:%M")

    # Logic to recommend clothing and accessories
    wind_level = _determine_level(WindSpeed, wind_speed_value_now)
    temp_level = _determine_level(TemperatureLevel, apparent_temp_value_now)

    utc_now = datetime.now(tz.tzutc())
    is_past_morning = utc_now > sunrise_time_utc + timedelta(minutes=30)
    is_before_evening = utc_now + timedelta(minutes=40) < sunrise_time_utc
    is_sunny = sky_cover_value_now < 30
    is_windy = wind_level in (WindSpeed.HIGH, WindSpeed.MEDIUM)

    items_to_bring = []
    if temp_level in (TemperatureLevel.VERY_COLD, TemperatureLevel.COLD):
        items_to_bring.extend(["Winter jacket", "Gloves", "Knit Hat"])
    elif temp_level == TemperatureLevel.COOL:
        items_to_bring.extend(["REI or OV pants", "T-shirt"])
    elif temp_level == TemperatureLevel.WARM:
        items_to_bring.extend(["Shorts", "T-shirt"])
    else:
        items_to_bring.extend(["Shorts", "T-shirt", "Hat"])

    if (is_past_morning and is_before_evening and is_sunny) or (is_windy and is_sunny):
        items_to_bring.extend(["Sunglasses"])

    if temp_level == TemperatureLevel.VERY_COLD and wind_level == WindSpeed.HIGH:
        items_to_bring.extend(["Facemask"])

    if probability_of_precipitation_value_now > 10 or quantitative_precipitation_value_now > 0:
        items_to_bring.extend(["Vivobarefoot shoes", "Umbrella"])

    items_string = ", ".join(items_to_bring)

    response = {"sunrise_time_utc": sunrise_time_short,
                "sunset_time_utc": sunset_time_short,
                "clothing_recs": items_string}
    return response
