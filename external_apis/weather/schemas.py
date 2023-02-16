from datetime import datetime
from typing import List

from dateutil.parser import parse
from dateutil import tz
from pydantic import BaseModel, Field, HttpUrl

from external_apis.weather.date_calculations import round_datetime_to_next_hour


class LocationMetadataProperties(BaseModel):
    forecast_grid_data_url: HttpUrl = Field(alias="forecastGridData")


class LocationMetadataResponse(BaseModel):
    properties: LocationMetadataProperties


class HourlyWeatherPropertyPeriodValues(BaseModel):
    valid_time: str = Field(alias="validTime")
    value: float

    @property
    def start_time(self) -> datetime:
        return parse(self.valid_time.split('/')[0])


class HourlyWeatherPropertyDetails(BaseModel):
    unit_of_measurement: str = Field(alias="uom")
    values: List[HourlyWeatherPropertyPeriodValues]

    def now_time_period_value(self) -> float:
        """
        Values have time period start times. Periods can be multiple hours.
        Logic finds the value for the time period that now is in.
        Also converts measurement value to Fahrenheit if needed
        Returns:
            period value
        """
        utc_now_rounded_hour = round_datetime_to_next_hour(datetime.now(tz.tzutc()))

        for period in reversed(self.values):
            if period.start_time <= utc_now_rounded_hour:
                if self.unit_of_measurement_value == "degC":
                    return (9 / 5) * period.value + 32
                else:
                    return period.value

    @property
    def unit_of_measurement_value(self) -> str:
        # ex format: 'wmoUnit:degC'
        return self.unit_of_measurement.split(":")[1]


class HourlyWeatherProperties(BaseModel):
    sky_cover: HourlyWeatherPropertyDetails = Field(alias="skyCover")
    apparent_temperature: HourlyWeatherPropertyDetails = Field(alias="apparentTemperature")
    probability_of_precipitation: HourlyWeatherPropertyDetails = Field(alias="probabilityOfPrecipitation")
    quantitative_precipitation: HourlyWeatherPropertyDetails = Field(alias="quantitativePrecipitation")
    wind_speed: HourlyWeatherPropertyDetails = Field(alias="windSpeed")


class HourlyWeatherResponse(BaseModel):
    properties: HourlyWeatherProperties
