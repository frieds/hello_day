from external_apis.weather.client import get_hourly_weather_details_now
from external_apis.sunrise_sunset.client import get_sunrise_sunset_times
from enum import Enum
from pydantic import BaseModel


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


def main():
    # hardcoded grid values for me
    grid_x = 34
    grid_y = 36
    weather_details_now = get_hourly_weather_details_now(grid_x, grid_y)

    is_rainy = True if "rain" in weather_details_now.short_forecast.lower() else False

    today_temperature_level = _determine_level(TemperatureLevel, weather_details_now.temperature)
    today_wind_level = _determine_level(WindSpeed, weather_details_now.wind_speed_mph_int)

    # hardcoded values for me
    sunrise_sunset_response = get_sunrise_sunset_times(40.752980, -73.929910)
    next_sunrise_local_time = sunrise_sunset_response.results.next_sunrise_local_time

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

    print(f"Next sunrise local time: {next_sunrise_local_time}")

main()
