"""Platform for sensor integration."""
from __future__ import annotations
import errno
from multiprocessing.connection import Client
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
from homeassistant.components.switch import (SwitchEntity)

class EctoSwitch(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    _api = None
    _item = None

    def __init__(self, hass: HomeAssistant, api: Api, item):
        self._is_on = True if item['state']['state']['val'] == 1 else False
        #self._attr_device_info = ...  # For automatic device registration
        #self._attr_unique_id = ...

        self._api = api
        self._item = item

        self._attr_name = item['config']['name']

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        self._is_on = True if self._api.getValue(self._item['id']) == 1 else False
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True
        self._api.setState(self._item['id'], "1")

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False
        self._api.setState(self._item['id'], "0")