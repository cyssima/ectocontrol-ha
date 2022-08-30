from __future__ import annotations
import errno
from multiprocessing.connection import Client
from .api import Api
from .const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import voluptuous as vol
import logging
from homeassistant.helpers import config_validation as cv, discovery

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
    }, extra=vol.ALLOW_EXTRA),
}, extra=vol.ALLOW_EXTRA)

async def async_setup(
    hass: HomeAssistant, 
    hass_config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None
) -> bool:

    config = hass_config[DOMAIN]

    hass.data[DOMAIN] = config

    await discovery.async_load_platform(hass, "sensor", DOMAIN, "", config)
    #await discovery.async_load_platform(hass, "switch", DOMAIN, "", config)

    return True