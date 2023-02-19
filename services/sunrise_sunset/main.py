from external_apis.sunrise_sunset.client import get_sunrise_sunset_times
from pydantic import BaseModel
from datetime import datetime


class SunriseSunsetTimesResponse(BaseModel):
    sunrise_time: datetime
    sunset_time: datetime


def get_sunrise_sunset_today_times_short(latitude: float, longitude: float):
    """
    Get sunrise and sunset times today in short datetime format like "2022-01-31 18:45" to be used in Apple Shortcut
    Args:
        latitude
        longitude
    Returns: dict with keys as sunrise and sunset times in short datetime format
    """
    sunrise_sunset_today_response = get_sunrise_sunset_times(latitude=latitude, longitude=longitude)
    sunrise_time_utc = sunrise_sunset_today_response.results.sunrise_time_utc
    sunset_time_utc = sunrise_sunset_today_response.results.sunset_time_utc

    sunset_time_short = sunset_time_utc.strftime("%Y-%m-%d %H:%M")
    sunrise_time_short = sunrise_time_utc.strftime("%Y-%m-%d %H:%M")

    response = SunriseSunsetTimesResponse(sunrise_time=sunrise_time_short, sunset_time=sunset_time_short)
    return response.dict()
