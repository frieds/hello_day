from requests import get
from requests.exceptions import HTTPError
from enum import Enum
from external_apis.weather.schemas import HourlyWeatherResponse, LocationMetadataResponse

_BASE_URL = "https://api.weather.gov"


class EndpointPath(str, Enum):
    LOCATION_METADATA = "/points/{latitude},{longitude}"


def _get_location_metadata(latitude: float, longitude: float):
    endpoint = EndpointPath.LOCATION_METADATA.format(latitude=latitude, longitude=longitude)
    url = f"{_BASE_URL}{endpoint}"
    try:
        response = get(url=url, headers={"User-Agent": "(local app, dfriedman33@gmail.com)"})
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise http_err
    return LocationMetadataResponse.parse_obj(response.json())


def _get_weather_forecast_grid_data(forecast_grid_data_url: str):
    try:
        response = get(url=forecast_grid_data_url, headers={"User-Agent": "(local app, dfriedman33@gmail.com)"})
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise http_err
    return HourlyWeatherResponse.parse_obj(response.json())


def get_hourly_weather(latitude: float, longitude: float):
    location_metadata_response = _get_location_metadata(latitude=latitude, longitude=longitude)
    forecast_data_grid_url = str(location_metadata_response.properties.forecast_grid_data_url)
    return _get_weather_forecast_grid_data(forecast_grid_data_url=forecast_data_grid_url)
    