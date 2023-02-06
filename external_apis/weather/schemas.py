from pydantic import BaseModel, Field
from typing import Any


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
