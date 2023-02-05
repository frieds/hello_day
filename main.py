from external_apis.weather.client import get_hourly_weather_details_now
from enum import Enum


class Calculations(Enum):
    def min(self):
        return self.value[0]

    def max(self):
        return self.value[1]
    

class TemperatureLevel(Calculations):
    VERY_COLD = (-100, 25)
    COLD = (25, 45)
    WARM = (45, 60)


class WindSpeed(Calculations):
    HIGH = (10, 100)
    MEDIUM = (5, 10)
    LOW = (0, 5)


def _determine_temperature_level(temperature):
    if TemperatureLevel.VERY_COLD.min() <= temperature < TemperatureLevel.VERY_COLD.max():
        level = TemperatureLevel.VERY_COLD
    elif TemperatureLevel.COLD.min() <= temperature < TemperatureLevel.COLD.max():
        level = TemperatureLevel.COLD
    else:
        level = TemperatureLevel.WARM
    return level


def _determine_wind_level(wind):
    if WindSpeed.HIGH.min() <= wind < WindSpeed.HIGH.max():
        level = WindSpeed.HIGH
    elif WindSpeed.MEDIUM.min() <= wind < WindSpeed.MEDIUM.max():
        level = WindSpeed.MEDIUM
    else:
        level = WindSpeed.LOW
    return level


def main():
    grid_x = 34
    grid_y = 36
    weather_details_now = get_hourly_weather_details_now(grid_x, grid_y)

    is_rainy = True if "rain" in weather_details_now.short_forecast.lower() else False

    today_temperature_level = _determine_temperature_level(weather_details_now.temperature)
    today_wind_level = _determine_wind_level(weather_details_now.wind_speed_mph_int)

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

main()

