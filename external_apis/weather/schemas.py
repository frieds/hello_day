from pydantic import BaseModel, Field, Extra
from typing import Any, List
from datetime import datetime
from dateutil.parser import parse


class HourlyWeatherPeriodDetails(BaseModel):
    number: int
    name: str
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")
    is_daytime: bool = Field(alias="isDaytime")
    temperature: int
    temperature_unit: str = Field(alias="temperatureUnit")
    temperature_trend: Any = Field(alias="temperatureTrend")
    wind_speed: str = Field(alias="windSpeed")
    wind_direction: str = Field(alias="windDirection")
    icon: str
    # A brief textual forecast summary for the period
    short_forecast: str = Field(alias="shortForecast")
    detailed_forecast: str = Field(alias="detailedForecast")

    @property
    def wind_speed_mph_int(self) -> int:
        return int(self.wind_speed.split()[0])


class HourlyWeatherProperties(BaseModel):
    updated: str
    units: str
    forecast_generator: str = Field(alias="forecastGenerator")
    generated_at: str = Field(alias="generatedAt")
    update_time: str = Field(alias="updateTime")
    valid_times: str = Field(alias="validTimes")
    elevation: dict
    periods: list[HourlyWeatherPeriodDetails]


class HourlyWeatherResponse(BaseModel):
    context: list = Field(alias="@context")
    type: str
    geometry: dict
    properties: HourlyWeatherProperties


class HourlyWeatherGranularPropertyPeriodValues(BaseModel):
    valid_time: str = Field(alias="validTime")
    value: float
    
    @property
    def start_time(self) -> datetime:
        return parse(self.valid_time.split('/')[0])
    

class HourlyWeatherGranularPropertyDetails(BaseModel):
    unit_of_measurement: str = Field(alias="uom")
    values: List[HourlyWeatherGranularPropertyPeriodValues]

    @property
    def unit_of_measurement_value(self) -> str:
        return self.unit_of_measurement.split(":")[1]

    @property
    def unit_of_measurement_value_full_name(self):
        # only mapped measurements for metrics used
        mapping = {"degC": "degrees_celsius",
                   "percent": "percent",
                   "mm": "millimeters",
                   "km_h-1": "kilometre_per_hour"
                   }
        return mapping[self.unit_of_measurement_value]
    

class HourlyWeatherGranularProperties(BaseModel, extra=Extra.allow):
    # arg of extra set to allow ignores tens of other fields
    sky_cover: HourlyWeatherGranularPropertyDetails = Field(alias="skyCover")
    apparent_temperature: HourlyWeatherGranularPropertyDetails = Field(alias="apparentTemperature")
    probability_of_precipitation: HourlyWeatherGranularPropertyDetails = Field(alias="probabilityOfPrecipitation")
    quantitative_precipitation: HourlyWeatherGranularPropertyDetails = Field(alias="quantitativePrecipitation")
    wind_speed: HourlyWeatherGranularPropertyDetails = Field(alias="windSpeed")
        

class HourlyWeatherGranularResponse(BaseModel):
    context: list = Field(alias="@context")
    type: str
    geometry: dict
    id: str
    properties: HourlyWeatherGranularProperties
