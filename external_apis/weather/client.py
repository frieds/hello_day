from requests import get
from requests.exceptions import HTTPError
from enum import Enum

from external_apis.weather.schemas import HourlyWeatherResponse, HourlyWeatherPeriodDetails

BASE_URL = "https://api.weather.gov"


class EndpointPath(str, Enum):
    HOURLY_FORECAST = "/gridpoints/OKX/{grid_x},{grid_y}/forecast/hourly"

    
def _get_hourly_forecast(grid_x: int, grid_y: int) -> HourlyWeatherResponse:
    endpoint = EndpointPath.HOURLY_FORECAST.format(grid_x=grid_x, grid_y=grid_y)
    url = f"{BASE_URL}{endpoint}"

    try:
        # User-Agent: (myweatherapp.com, contact@myweatherapp.com)
        response = get(url=url, )
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise http_err
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise err

    return HourlyWeatherResponse.parse_obj(response.json())


def get_hourly_weather_details_now(grid_x: int, grid_y: int) -> HourlyWeatherPeriodDetails:
    # assumption is first period is relevant weather now
    hourly_weather_response = _get_hourly_forecast(grid_x, grid_y)
    return hourly_weather_response.properties.periods[0]








