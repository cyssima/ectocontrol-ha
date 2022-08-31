"""Platform for sensor integration."""
from __future__ import annotations
import errno
from multiprocessing.connection import Client
from .const import DOMAIN
from .api import Api

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
import homeassistant.const
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, hass_config, async_add_entities, discovery_info=None):
    api = hass.data[DOMAIN]
    api.setClientSession(async_get_clientsession(hass))
    token = await api.getToken()

    if not token:
        _LOGGER.error("Could not connect to EctoControl")
        return

    items = await api.getItems()
    entities = []
    for item in items:
        if item['info']['type']['type'] != 6946:
            entities.extend([EctoSensor(hass, api, item)])

    async_add_entities(entities)

class EctoSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = None
    _attr_native_unit_of_measurement = None
    _attr_device_class = None
    _attr_state_class = SensorStateClass.MEASUREMENT

    _api = None
    _item = None

    async def async_update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = await self._api.getValue(self._item['id'])

    def __init__(self, hass: HomeAssistant, api: Api, item):
        self._api = api
        self._item = item

        self._attr_name = item['config']['name']

        if item['info']['type']['type'] == 1889:
            self._attr_native_unit_of_measurement = homeassistant.const.TEMP_CELSIUS
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
        if item['info']['type']['type'] == 737:
            self._attr_device_class = SensorDeviceClass.CURRENT
        if item['info']['type']['type'] == 321:
            self._attr_native_unit_of_measurement = homeassistant.const.PERCENTAGE
            self._attr_device_class = SensorDeviceClass.BATTERY
        if item['info']['type']['type'] == 1857:            
            self._attr_device_class = SensorDeviceClass.CURRENT