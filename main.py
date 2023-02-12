from external_apis.weather.client import get_hourly_weather_details_now
from external_apis.sunrise_sunset.client import get_sunrise_sunset_times
from enum import Enum
from pydantic import BaseModel
from datetime import datetime, timedelta, date
from dateutil import tz


class Range(BaseModel):
    min: int
    max: int


class TemperatureLevel(Enum):
    VERY_COLD = Range(min=-100, max=25)
    COLD = Range(min=25, max=45)
    WARM = Range(min=45, max=60)


class WindSpeed(Enum):
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


def _determine_relevant_sunrise_date() -> date:
    """Returns today's date if time now is between 4-7:30am; else, tomorrow date"""
    local_tz = tz.tzlocal()
    local_time_now = datetime.now(local_tz)
    if 4 <= local_time_now.hour < 7 or (local_time_now.hour == 7 and local_time_now.minute < 30):
        relevant_date = local_time_now.date()
    else:
        relevant_date = local_time_now.date() + timedelta(days=1)
    return relevant_date


def _date_human_readable_string(a_datetime: datetime):
    """Convert datetime into format like 6:51am today or 6:30am tomorrow"""
    local_tz = tz.tzlocal()

    # Get today's and tomorrow's date in the local time zone
    today = datetime.now(local_tz).date()
    tomorrow = today + timedelta(days=1)

    datetime_hour_minute = a_datetime.strftime("%-H:%M%p").lower()
    if a_datetime.date() == today:
        date_str = "today"
    elif a_datetime.date() == tomorrow:
        date_str = "tomorrow"

    return f"{datetime_hour_minute} {date_str}"


def main():
    # hardcoded grid values for me
    grid_x = 34
    grid_y = 36
    weather_details_now = get_hourly_weather_details_now(grid_x, grid_y)

    is_rainy = True if "rain" in weather_details_now.short_forecast.lower() else False

    today_temperature_level = _determine_level(TemperatureLevel, weather_details_now.temperature)
    today_wind_level = _determine_level(WindSpeed, weather_details_now.wind_speed_mph_int)

    relevant_sunrise_date = _determine_relevant_sunrise_date()
    # hardcoded values for me
    sunrise_sunset_response = get_sunrise_sunset_times(40.752980, -73.929910, relevant_sunrise_date)
    local_tz = tz.tzlocal()
    utc_sunrise_time = sunrise_sunset_response.results.sunrise
    est_sunrise_time = utc_sunrise_time.astimezone(local_tz)
    sunrise_statement = _date_human_readable_string(est_sunrise_time)    

    print("Wear:")
    if today_temperature_level in (TemperatureLevel.VERY_COLD, TemperatureLevel.COLD):
        print("Winter jacket", "Gloves", "Knit Hat", sep="\n")
    else:
        print("REI or OV pants", "T-shirt", sep="\n")

    if today_wind_level in (WindSpeed.HIGH, WindSpeed.MEDIUM) and weather_details_now.is_daytime:
        print("Sunglasses")

    if today_temperature_level == TemperatureLevel.VERY_COLD and today_wind_level == WindSpeed.HIGH:
        print("Facemask")

    if is_rainy:
        print("Vivobarefoot shoes, Umbrella", sep="\n")

    print(f"Next sunrise: {sunrise_statement}")


main()
