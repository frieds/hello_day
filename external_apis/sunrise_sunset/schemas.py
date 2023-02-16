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

    @property
    def sunrise_time_human_readable(self):
        return self.get_humanized_time_string(self.sunrise_time_utc)

    @property
    def sunset_time_human_readable(self):
        return self.get_humanized_time_string(self.sunset_time_utc)

    @classmethod
    def get_humanized_time_string(cls, datetime_value_utc: datetime):
        # convert to local time
        datetime_value_local = datetime_value_utc.astimezone(tz.tzlocal())
        # converts to hour:minute am/pm
        datetime_hour_minute = datetime_value_local.strftime("%-I:%M%p").lower()

        datetime_now_utc = datetime.now(tz.tzutc())

        if datetime_value_utc > datetime_now_utc:
            output = f"is today at {datetime_hour_minute}"
        elif datetime_value_utc > datetime_now_utc + timedelta(minutes=30):
            output = f"was earlier at {datetime_hour_minute}"
        else:
            output = f"was way earlier at {datetime_hour_minute}"
        return output


class SunriseSunsetResponse(BaseModel):
    results: SunriseSunset
    status: str
