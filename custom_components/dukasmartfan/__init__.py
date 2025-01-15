"""
Duka Smartfan Integration.

see http://www.dingus.dk for more information
"""
import asyncio
import logging

import voluptuous as vol
from duka_smartfan_sdk.dukaclient import Device, DukaClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent

from .const import DOMAIN

from homeassistant.const import Platform 

PLATFORMS = [
    Platform.FAN,
    Platform.SENSOR,
] 

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)


def setup(hass: HomeAssistant, config: dict):
    """Set up the Duka Smartfan component."""

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = DukaEntityComponent(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Duka Smartfan from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, "fan"),
                hass.config_entries.async_forward_entry_unload(entry, "sensor"),
            ]
        )
    )

    return unload_ok


class DukaEntityComponent(EntityComponent):
    """We only want to have one instance of the dukaclient."""

    def __init__(self, hass):
        super(DukaEntityComponent, self).__init__(_LOGGER, DOMAIN, hass)
        self._client = None

    @property
    def client(self) -> DukaClient:
        """Get the duka smartfan client."""
        if self._client is None:
            self._client = DukaClient()
        return self._client
