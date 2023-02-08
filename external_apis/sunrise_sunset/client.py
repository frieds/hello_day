from requests import get
from enum import Enum
from requests.exceptions import HTTPError

from external_apis.sunrise_sunset.schemas import SunriseSunsetResponse

_BASE_URL = "https://api.sunrise-sunset.org"


class EndpointPath(str, Enum):
    # formatted=0 ensures datetimes in ISO 8601 format and day_length in seconds
    SUNRISE_SUNSET_TIMES = "/json?lat={latitude}&lng={longitude}&formatted=0"


def get_sunrise_sunset_times(latitude: float, longitude: float) -> SunriseSunsetResponse:
    endpoint = EndpointPath.SUNRISE_SUNSET_TIMES.format(latitude=latitude, longitude=longitude)
    url = f"{_BASE_URL}{endpoint}"

    try:
        response = get(url=url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise http_err

    return SunriseSunsetResponse.parse_obj(response.json())