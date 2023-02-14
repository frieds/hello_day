from typing import Optional
from requests import get
from requests.exceptions import HTTPError
from datetime import date

from external_apis.sunrise_sunset.schemas import SunriseSunsetResponse, SunriseSunsetQueryParams

_BASE_URL = "https://api.sunrise-sunset.org/json"


def get_sunrise_sunset_times(latitude: float, longitude: float, date_value: Optional[date] = None) -> SunriseSunsetResponse:
    query_params = SunriseSunsetQueryParams(latitude=latitude, longitude=longitude, date_value=date_value)
    query_params_dict = query_params.dict(exclude_none=True, by_alias=True)
    try:
        response = get(url=_BASE_URL, params=query_params_dict)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise http_err

    return SunriseSunsetResponse.parse_obj(response.json())