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
from homeassistant.helpers.entity import EntityCategory, ATTR_DEVICE_CLASS

mdis = {
    21948:{1:"mdi:water-pump",0:"mdi:water-pump-off"},
    0:{1:"mdi:toggle-switch",0:"mdi:toggle-switch-off"}
}

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
        #self._attr_entity_category = EntityCategory.CONFIG
        #self._attr_device_class

        self._api.setDispatcher(self._item['id'], self.set_state)

    def set_state(self, state):
        self._attr_is_on = True if state == 1 else False
        if self._attr_unique_id in mdis:
            self._attr_icon = mdis[self._attr_unique_id][state]
        else:
            self._attr_icon = mdis[0][state]

    async def async_turn_on(self):
        await self._api.setState(self._item['id'], "1")
        self.set_state(1)

    async def async_turn_off(self):
        await self._api.setState(self._item['id'], "0")
        self.set_state(0)