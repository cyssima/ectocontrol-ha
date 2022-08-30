"""Platform for sensor integration."""
from __future__ import annotations
import errno
from multiprocessing.connection import Client
from .api import Api
from .const import DOMAIN

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
        #self._attr_device_info = ...  # For automatic device registration
        
        self._api = api
        self._item = item

        self._attr_name = item['config']['name']
        self._attr_unique_id = self._item['id']

        self._api.setDispatcher(self._item['id'], self.set_state)

    def set_state(self, state):
        self._attr_is_on = True if state == 1 else False

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._api.setState(self._item['id'], "1")
        self.set_state(1)

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._api.setState(self._item['id'], "0")
        self.set_state(0)