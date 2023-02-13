from requests import get
from requests.exceptions import HTTPError
from enum import Enum
from datetime import datetime

from external_apis.weather.schemas import HourlyWeatherResponse, HourlyWeatherPeriodDetails, \
    HourlyWeatherGranularResponse

_BASE_URL = "https://api.weather.gov"


class EndpointPath(str, Enum):
    HOURLY_FORECAST = "/gridpoints/OKX/{grid_x},{grid_y}/forecast/hourly"
    HOURLY_GRANULAR = "/gridpoints/LWX/{grid_x},{grid_y}"


def get_hourly_granular(grid_x: int, grid_y: int):
    endpoint = EndpointPath.HOURLY_GRANULAR.format(grid_x=grid_x, grid_y=grid_y)
    url = f"{_BASE_URL}{endpoint}"

    try:
        response = get(url=url, headers={"User-Agent": "(local app, dfriedman33@gmail.com)"})
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise http_err
    return HourlyWeatherGranularResponse.parse_obj(response.json())
    
    
def _get_hourly_forecast(grid_x: int, grid_y: int) -> HourlyWeatherResponse:
    endpoint = EndpointPath.HOURLY_FORECAST.format(grid_x=grid_x, grid_y=grid_y)
    url = f"{_BASE_URL}{endpoint}"

    try:
        response = get(url=url, headers={"User-Agent": "(local app, dfriedman33@gmail.com)"})
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise http_err

    return HourlyWeatherResponse.parse_obj(response.json())


def get_hourly_weather_details_now(grid_x: int, grid_y: int) -> HourlyWeatherPeriodDetails:
    """Assumption is first period is relevant weather now"""
    hourly_weather_response = _get_hourly_forecast(grid_x, grid_y)
    return hourly_weather_response.properties.periods[0]
