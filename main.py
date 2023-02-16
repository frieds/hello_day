from datetime import datetime, timedelta
from enum import Enum

from dateutil import tz
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


def main():
    # hardcoded values for me
    latitude = 40.752980
    longitude = -73.929910

    utc_now = datetime.now(tz.tzutc())

    # Get weather metrics
    weather_details = get_hourly_weather(latitude=latitude, longitude=longitude)

    apparent_temp_value_now = weather_details.properties.apparent_temperature.now_time_period_value()
    wind_speed_value_now = weather_details.properties.wind_speed.now_time_period_value()
    probability_of_precipitation_value_now = weather_details.properties.probability_of_precipitation.now_time_period_value()
    quantitative_precipitation_value_now = weather_details.properties.quantitative_precipitation.now_time_period_value()
    sky_cover_value_now = weather_details.properties.sky_cover.now_time_period_value()

    # Get sunrise and sunset data
    sunrise_sunset_today_response = get_sunrise_sunset_times(latitude=latitude, longitude=longitude)
    sunset_sunrise_data = sunrise_sunset_today_response.results
    sunrise_time_utc = sunset_sunrise_data.sunrise_time_utc

    sunrise_time_human_readable = sunset_sunrise_data.sunrise_time_human_readable
    sunset_time_human_readable = sunset_sunrise_data.sunset_time_human_readable

    # Logic to recommend clothing and accessories

    wind_level = _determine_level(WindSpeed, wind_speed_value_now)
    temp_level = _determine_level(TemperatureLevel, apparent_temp_value_now)

    is_past_morning = utc_now > sunrise_time_utc + timedelta(minutes=30)
    is_before_evening = utc_now + timedelta(minutes=40) < sunrise_time_utc
    is_sunny = sky_cover_value_now < 30
    is_windy = wind_level in (WindSpeed.HIGH, WindSpeed.MEDIUM)

    print("Wear:")
    if temp_level in (TemperatureLevel.VERY_COLD, TemperatureLevel.COLD):
        print("Winter jacket", "Gloves", "Knit Hat", sep="\n")
    elif temp_level == TemperatureLevel.COOL:
        print("REI or OV pants", "T-shirt", sep="\n")
    elif temp_level == TemperatureLevel.WARM:
        print("Shorts", "T-shirt", sep="\n")
    else:
        print("Shorts", "T-shirt", "Hat", sep="\n")

    if (is_past_morning and is_before_evening and is_sunny) or (is_windy and is_sunny):
        print("Sunglasses")

    if temp_level == TemperatureLevel.VERY_COLD and wind_level == WindSpeed.HIGH:
        print("Facemask")

    if probability_of_precipitation_value_now > 10 or quantitative_precipitation_value_now > 0:
        print("Vivobarefoot shoes, Umbrella", sep="\n")

    print(f"\nSunrise {sunrise_time_human_readable}")
    print(f"Sunset {sunset_time_human_readable}")


main()
