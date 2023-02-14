from pydantic import BaseModel, Field
from datetime import datetime, date
from dateutil import tz
from typing import Union


class SunriseSunsetQueryParams(BaseModel):
    latitude: float
    longitude: float
    # API default is date will be today
    date_value: Union[date, None] = None
    formatted: int = 0

    def to_query_param_names(self):
        # keys are query param names from API endpoint
        query_params = {
            "lat": self.latitude,
            "lng": self.longitude,
            "formatted": self.formatted
        }
        if self.date_value is not None:
            query_params["date"] = self.date_value
        return query_params


class SunriseSunset(BaseModel):
    # all times UTC
    sunrise_time_utc: datetime = Field(alias="sunrise")
    sunset_time_utc: datetime = Field(alias="sunset")
    solar_noon: datetime
    # in seconds
    day_length: int
    civil_twilight_begin: datetime
    civil_twilight_end: datetime
    nautical_twilight_begin: datetime
    nautical_twilight_end: datetime
    astronomical_twilight_begin: datetime
    astronomical_twilight_end: datetime

    @property
    def next_sunrise_local_time(self) -> datetime:
        local_tz = tz.tzlocal()
        return self.sunrise.astimezone(local_tz)
    

class SunriseSunsetResponse(BaseModel):
    results: SunriseSunset
    status: str
