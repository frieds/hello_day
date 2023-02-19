from enum import Enum
from pydantic import BaseModel


class Range(BaseModel):
    min: int
    max: int


class TemperatureLevel(Enum):
    # min max values in Fahrenheit
    VERY_COLD = Range(min=-100, max=25)
    COLD = Range(min=25, max=45)
    COOL = Range(min=45, max=57)
    WARM = Range(min=57, max=67)
    HOT = Range(min=67, max=100)


class WindSpeed(Enum):
    # min max values in miles per hour (mph)
    HIGH = Range(min=10, max=100)
    MEDIUM = Range(min=5, max=10)
    LOW = Range(min=0, max=5)