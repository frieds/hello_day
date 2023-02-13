from requests import get
from requests.exceptions import HTTPError
from datetime import date

from external_apis.sunrise_sunset.schemas import SunriseSunsetResponse, SunriseSunsetQueryParams

_BASE_URL = "https://api.sunrise-sunset.org/json"


def get_sunrise_sunset_times(latitude: float, longitude: float, a_date: date) -> SunriseSunsetResponse:
    query_params = SunriseSunsetQueryParams(latitude=latitude, longitude=longitude, date=a_date)
    
    try:
        response = get(url=_BASE_URL, params=query_params.to_query_param_names())
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise http_err

    return SunriseSunsetResponse.parse_obj(response.json())
