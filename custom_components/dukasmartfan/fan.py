"""
Platform for Duka Smartfan fan.

see http://www.dingus.dk for more information
"""
import asyncio
import logging
import time

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from duka_smartfan_sdk.device import Device
from homeassistant.components.fan import PLATFORM_SCHEMA, FanEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_DEVICE_ID,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
)
from homeassistant.helpers import entity_platform
from homeassistant.helpers.typing import HomeAssistantType

from .dukaentity import DukaEntity

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_DEVICE_ID): cv.string,
        vol.Optional(CONF_PASSWORD, default="1111"): cv.string,
        vol.Optional(CONF_IP_ADDRESS, default="<broadcast>"): cv.string,
    }
)
TOGGLE_BOOST_SCHEMA = vol.Schema({vol.Required(ATTR_ENTITY_ID): cv.entity_ids})


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Duka One based on a config entry."""

    name = entry.data[CONF_NAME]
    device_id = entry.data[CONF_DEVICE_ID]
    password = entry.data[CONF_PASSWORD]
    ip_address = entry.data[CONF_IP_ADDRESS]
    if ip_address is None or len(ip_address) == 0:
        ip_address = "<broadcast>"

    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        "toggle_boost", TOGGLE_BOOST_SCHEMA, "toggle_boost"
    )
    dukasmartfanfan = DukaSmartFanFan(hass, name, device_id, password, ip_address)
    await dukasmartfanfan.wait_for_device_to_be_ready()
    async_add_entities([dukasmartfanfan], True)


class DukaSmartFanFan(FanEntity, DukaEntity):
    """A Duka Smartfan fan component."""

    def __init__(self, hass: HomeAssistantType, name, device_id, password, ip_address):
        """Initialize the Duka Smartfan fan."""
        super(DukaSmartFanFan, self).__init__(hass, device_id)
        self._name = name
        self._supported_features = 0
        hass.async_add_executor_job(self.initialize_device, password, ip_address)

    async def async_will_remove_from_hass(self):
        """Unsubscribe when removed."""
        self.device = self.client.remove_device(self.device)
        return

    def on_change(self, device: Device):
        """Callback when the duka smartfan change state"""
        if self.hass is not None:
            self.schedule_update_ha_state()
        return

    @property
    def name(self):
        """Return then name"""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id

    @property
    def should_poll(self):
        """No polling needed for a Duka Smartfan fan."""
        return False

    @property
    def assumed_state(self):
        """Return false  if we do optimistic updates."""
        return False

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._supported_features

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.device is None or not self.device.is_initialized():
            return {}
        return {
            "temperature": self.device.temperature,
            "fan_speed": self.device.fan_speed,
            "humidity": self.device.humidity,
        }

    def turn_on(
        self,
        **kwargs,
    ) -> None:
        """Turn on the entity."""
        self.client.turn_on(self.device)

    def turn_off(self, **kwargs) -> None:
        """Turn off the entity."""
        self.client.turn_off(self.device)

    def toggle_boost(self, **kwargs) -> None:
        self.client.toggle_boost(self.device)

    @property
    def device_info(self):
        return self.dukasmartfan_device_info()
