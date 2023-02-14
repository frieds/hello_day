from external_apis.weather.client import get_hourly_granular
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


def _round_datetime_to_hour(a_datetime):
    if a_datetime.minute >= 45:
        a_datetime = a_datetime.replace(hour=a_datetime.hour + 1, minute=0, second=0, microsecond=0)
    else:
        a_datetime = a_datetime.replace(minute=0, second=0, microsecond=0)
    return a_datetime


def _determine_now_time_period_value(metric_period_values, rounded_utc_hour_now) -> float:
    for period in reversed(metric_period_values):
        if period.start_time <= rounded_utc_hour_now:
            return period.value


def main():
    # hardcoded values for me
    grid_x = 34
    grid_y = 36
    latitude = 40.752980
    longitude = -73.929910

    weather_granular_details = get_hourly_granular(grid_x, grid_y)

    utc_now = datetime.now(tz.tzutc())
    rounded_utc_hour_now = _round_datetime_to_hour(utc_now)

    apparent_temp_period_values = weather_granular_details.properties.apparent_temperature.values
    apparent_temp_value_now = _determine_now_time_period_value(apparent_temp_period_values, rounded_utc_hour_now)

    wind_speed_period_values = weather_granular_details.properties.wind_speed.values
    wind_speed_value_now = _determine_now_time_period_value(wind_speed_period_values, rounded_utc_hour_now)

    probability_of_precipitation_period_values = weather_granular_details.properties.probability_of_precipitation.values
    probability_of_precipitation_value_now = _determine_now_time_period_value(probability_of_precipitation_period_values
                                                                              , rounded_utc_hour_now)

    quantitative_precipitation_period_values = weather_granular_details.properties.quantitative_precipitation.values
    quantitative_precipitation_value_now = _determine_now_time_period_value(quantitative_precipitation_period_values,
                                                                            rounded_utc_hour_now)

    sky_cover_period_values = weather_granular_details.properties.sky_cover.values
    sky_cover_value_now = _determine_now_time_period_value(sky_cover_period_values, rounded_utc_hour_now)

    relevant_sunrise_date = _determine_relevant_sunrise_date()
    sunrise_sunset_response = get_sunrise_sunset_times(latitude=latitude, longitude=longitude,
                                                       date_value=relevant_sunrise_date)
    local_tz = tz.tzlocal()
    utc_sunrise_time = sunrise_sunset_response.results.sunrise
    est_sunrise_time = utc_sunrise_time.astimezone(local_tz)
    sunrise_statement = _date_human_readable_string(est_sunrise_time)

    date_today = utc_now.date()
    sunrise_sunset_today_response = get_sunrise_sunset_times(latitude=latitude, longitude=longitude, date_value=date_today)
    utc_sunrise_today_time = sunrise_sunset_today_response.results.sunrise
    utc_sunset_today_time = sunrise_sunset_today_response.results.sunset

    is_past_morning = utc_now > utc_sunrise_today_time + timedelta(minutes=30)
    is_before_evening = utc_now + timedelta(minutes=40) < utc_sunset_today_time
    is_sunny = sky_cover_value_now < 30
    is_windy = wind_speed_value_now in (WindSpeed.HIGH, WindSpeed.MEDIUM)
    
    print("Wear:")
    if apparent_temp_value_now in (TemperatureLevel.VERY_COLD, TemperatureLevel.COLD):
        print("Winter jacket", "Gloves", "Knit Hat", sep="\n")
    else:
        print("REI or OV pants", "T-shirt", sep="\n")
        
    if (is_past_morning and is_before_evening and is_sunny) or (is_windy and is_sunny):
        print("Sunglasses")

    if apparent_temp_value_now == TemperatureLevel.VERY_COLD and wind_speed_value_now == WindSpeed.HIGH:
        print("Facemask")

    if probability_of_precipitation_value_now > 10 or quantitative_precipitation_value_now > 0:
        print("Vivobarefoot shoes, Umbrella", sep="\n")

    print(f"Next sunrise: {sunrise_statement}")


main()
