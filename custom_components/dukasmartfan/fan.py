"""
Platform for Duka Smartfan fan.

see http://www.dingus.dk for more information
"""

import logging

from duka_smartfan_sdk.device import Device
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.device_registry import DeviceInfo

from .dukaentity import DukaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Duka One based on a config entry."""

    name = entry.data[CONF_NAME]
    device_id = entry.data[CONF_DEVICE_ID]
    password = entry.data[CONF_PASSWORD]
    ip_address = entry.data[CONF_IP_ADDRESS]
    if ip_address is None or len(ip_address) == 0:
        ip_address = "<broadcast>"

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service("toggle_boost", {}, "toggle_boost")
    dukasmartfanfan = DukaSmartFanFan(hass, name, device_id, password, ip_address)
    await dukasmartfanfan.wait_for_device_to_be_ready()
    async_add_entities([dukasmartfanfan], True)


class DukaSmartFanFan(FanEntity, DukaEntity):
    """A Duka Smartfan fan component."""

    _attr_supported_features = FanEntityFeature.TURN_ON | FanEntityFeature.TURN_OFF
    _attr_should_poll = False
    _attr_assumed_state = False

    def __init__(self, hass: HomeAssistant, name, device_id, password, ip_address):
        """Initialize the Duka Smartfan fan."""
        super(DukaSmartFanFan, self).__init__(hass, device_id)
        self._attr_name = name
        self._is_active = None
        hass.async_add_executor_job(self.initialize_device, password, ip_address)

    async def async_will_remove_from_hass(self):
        """Unsubscribe when removed."""
        self.device = self.client.remove_device(self.device)
        return

    def on_change(self, device: Device):
        """Callback when the duka smartfan change state"""
        has_changed = False
        if self._is_active != device.is_active:
            self._is_active = device.is_active
            has_changed = True
        if self.hass is not None and has_changed:
            self.schedule_update_ha_state()

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id

    @property
    def is_on(self):
        """
        Use is_active as proxy for is_on.
        """
        return self._is_active

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
    def device_info(self) -> DeviceInfo | None:
        return self.dukasmartfan_device_info()
