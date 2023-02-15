from requests import get
from requests.exceptions import HTTPError
from enum import Enum

from external_apis.weather.schemas import HourlyWeatherGranularResponse, LocationMetadataResponse, \
    LocationMetadataProperties

_BASE_URL = "https://api.weather.gov"


class EndpointPath(str, Enum):
    HOURLY_GRANULAR = "/gridpoints/LWX/{grid_x},{grid_y}"
    LOCATION_METADATA = "/points/{latitude},{longitude}"


def get_location_metadata(latitude: float, longitude: float):
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
