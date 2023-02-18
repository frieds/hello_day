from datetime import date, datetime, timedelta
from typing import Union

from dateutil import tz
from pydantic import BaseModel, Field


class SunriseSunsetQueryParams(BaseModel):
    latitude: float = Field(alias="lat")
    longitude: float = Field(alias="lng")
    # API default is date will be today
    date_value: Union[date, None] = Field(default=None, alias="date")
    formatted: int = 0

    class Config:
        allow_population_by_field_name = True


class SunriseSunset(BaseModel):
    # all times UTC
    sunrise_time_utc: datetime = Field(alias="sunrise")
    sunset_time_utc: datetime = Field(alias="sunset")
    # in seconds
    day_length: int


class SunriseSunsetResponse(BaseModel):
    results: SunriseSunset
    status: str
