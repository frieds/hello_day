from pydantic import BaseModel, Field
from datetime import datetime, date
from dateutil import tz


class SunriseSunsetQueryParams(BaseModel):
    latitude: float
    longitude: float
    date: date
    formatted: int = 0

    def to_query_param_names(self):
        return {
            "lat": self.latitude,
            "lng": self.longitude,
            "date": self.date,
            "formatted": self.formatted
        }


class SunriseSunset(BaseModel):
    # all times UTC
    sunrise: datetime
    sunset: datetime
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
