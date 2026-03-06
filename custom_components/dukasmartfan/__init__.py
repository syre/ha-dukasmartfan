"""
Duka Smartfan Integration.

see http://www.dingus.dk for more information
"""

import logging

from duka_smartfan_sdk.dukaclient import DukaClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS = [
    Platform.FAN,
    Platform.SENSOR,
]

_LOGGER = logging.getLogger(__name__)


class DukaData:
    """Hold the Duka Smartfan client instance."""

    def __init__(self):
        self._client = None

    @property
    def client(self) -> DukaClient:
        """Get the duka smartfan client."""
        if self._client is None:
            self._client = DukaClient()
        return self._client


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Duka Smartfan component."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = DukaData()
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Duka Smartfan from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = DukaData()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
