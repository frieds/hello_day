from pydantic import BaseModel, Field, Extra, HttpUrl
from typing import List
from datetime import datetime
from dateutil.parser import parse


class LocationMetadataProperties(BaseModel):
    forecast_grid_data_url: HttpUrl = Field(alias="forecastGridData")


class LocationMetadataResponse(BaseModel):
    properties: LocationMetadataProperties


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
