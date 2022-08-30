from datetime import timedelta
from typing import Final

from homeassistant.components.sensor import DOMAIN as SENSOR
from homeassistant.components.weather import ATTR_FORECAST_CONDITION
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    ATTR_NAME,
    ATTR_UNIT_OF_MEASUREMENT,
    DEGREE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    LENGTH_MILLIMETERS,
    PERCENTAGE,
    PRESSURE_HPA,
    SPEED_METERS_PER_SECOND,
    TEMP_CELSIUS,
)

# Base component constants
NAME: Final = "EctoControl"
DOMAIN: Final = "ectocontrol"
VERSION: Final = "0.1.0-alpha"
ATTRIBUTION: Final = "Data provided by EctoControl"

STARTUP_MESSAGE: Final = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
-------------------------------------------------------------------
"""

# Platforms
PLATFORMS: Final = [SENSOR]

# Defaults
DEFAULT_NAME: Final = "EctoControl"

# Attributes
ATTR_LAST_UPDATED: Final = "last_updated"

ENDPOINT_URL: Final = "https://my.ectostroy.ru/api"

UPDATE_INTERVAL: Final = timedelta(minutes=1)

DEVICE_CLASS_TPL: Final = DOMAIN + "__{}"

SENSOR_TYPES: Final = {
    "temperature": {
        ATTR_DEVICE_CLASS: DEVICE_CLASS_TEMPERATURE,
        ATTR_ICON: None,
        ATTR_NAME: "Temperature",
        ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
    }
}
