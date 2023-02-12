from pydantic import BaseModel, Field
from datetime import datetime
from dateutil import tz


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



