from datetime import datetime
from typing import List

from dateutil.parser import parse
from pydantic import BaseModel, Field, HttpUrl


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

    @property
    def unit_of_measurement_value(self) -> str:
        return self.unit_of_measurement.split(":")[1]

    @property
    def unit_of_measurement_value_full_name(self):
        # only mapped measurements for metrics used
        mapping = {
            "degC": "degrees_celsius",
            "percent": "percent",
            "mm": "millimeters",
            "km_h-1": "kilometre_per_hour"
        }
        return mapping[self.unit_of_measurement_value]


class HourlyWeatherProperties(BaseModel):
    sky_cover: HourlyWeatherPropertyDetails = Field(alias="skyCover")
    apparent_temperature: HourlyWeatherPropertyDetails = Field(alias="apparentTemperature")
    probability_of_precipitation: HourlyWeatherPropertyDetails = Field(alias="probabilityOfPrecipitation")
    quantitative_precipitation: HourlyWeatherPropertyDetails = Field(alias="quantitativePrecipitation")
    wind_speed: HourlyWeatherPropertyDetails = Field(alias="windSpeed")


class HourlyWeatherResponse(BaseModel):
    properties: HourlyWeatherProperties
