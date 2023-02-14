from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Union


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
    solar_noon: datetime
    # in seconds
    day_length: int
    civil_twilight_begin: datetime
    civil_twilight_end: datetime
    nautical_twilight_begin: datetime
    nautical_twilight_end: datetime
    astronomical_twilight_begin: datetime
    astronomical_twilight_end: datetime


class SunriseSunsetResponse(BaseModel):
    results: SunriseSunset
    status: str
