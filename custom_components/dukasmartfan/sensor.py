"""
Sensor platform for Duka Smartfan fan.

see http://www.dingus.dk for more information
"""

import asyncio
import logging
import time

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant

from .dukaentity import DukaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Duka Smartfan humidity sensor and temperature sensor based on a config entry."""

    name = entry.data[CONF_NAME]
    device_id = entry.data[CONF_DEVICE_ID]
    duka_smartfan_humidity_sensor = DukaSmartfanHumidity(
        hass, name + " humidity", device_id
    )
    duka_smartfan_temperature_sensor = DukaSmartfanTemperature(
        hass, name + " temperature", device_id
    )
    if not (
        await duka_smartfan_humidity_sensor.wait_for_device_to_be_ready()
        or await duka_smartfan_temperature_sensor.wait_for_device_to_be_ready()
    ):
        _LOGGER.error("Failed to setup dukasmartfan device")
        return False
    async_add_entities(
        [duka_smartfan_humidity_sensor, duka_smartfan_temperature_sensor], True
    )


class DukaSmartfanHumidity(Entity, DukaEntity):
    """A Duka Smartfan humidity sensor entity."""

    def __init__(self, hass: HomeAssistant, name: str, device_id: str):
        """Initialize the Duka Smartfan fan."""
        super(DukaSmartfanHumidity, self).__init__(hass, device_id)
        self._name = name

    async def wait_for_device_to_be_ready(self):
        """Wait for the device to be initialized.

        Then wait until the first humidity command has been received"""
        _LOGGER.debug("Waiting to get dukasmartfan device")
        timeout = time.time() + 10
        while True:
            self.device = self.client.get_device(self._device_id)
            if self.device is not None:
                break
            if time.time() > timeout:
                return False
            await asyncio.sleep(0.1)
        _LOGGER.debug("Waiting for dukasmartfan sensor device")
        if not await super(DukaSmartfanHumidity, self).wait_for_device_to_be_ready():
            return False
        _LOGGER.debug("Waiting for dukasmartfan humidity sensor")
        timeout = time.time() + 10
        while self.device is None or self.device.humidity is None:
            if time.time() > timeout:
                _LOGGER.warning("Timeout waiting for humidity reply")
                return False
            await asyncio.sleep(0.1)
        return True

    @property
    def name(self):
        """Return the name"""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id + "_humidity"

    @property
    def should_poll(self):
        """We poll because the fan handle changes."""
        return True

    @property
    def assumed_state(self):
        """Return false if we do optimistic updates."""
        return False

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.device.humidity

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity"""
        return "%"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:water-percent"

    @property
    def device_info(self):
        return self.dukasmartfan_device_info()


class DukaSmartfanTemperature(Entity, DukaEntity):
    """A Duka Smartfan humidity sensor entity."""

    def __init__(self, hass: HomeAssistant, name: str, device_id: str):
        """Initialize the Duka Smartfan fan."""
        super(DukaSmartfanTemperature, self).__init__(hass, device_id)
        self._name = name

    async def wait_for_device_to_be_ready(self):
        """Wait for the device to be initialized.

        Then wait until the first temperature command has been received"""
        _LOGGER.debug("Waiting to get dukasmartfan device")
        timeout = time.time() + 10
        while True:
            self.device = self.client.get_device(self._device_id)
            if self.device is not None:
                break
            if time.time() > timeout:
                return False
            await asyncio.sleep(0.1)
        _LOGGER.debug("Waiting for dukasmartfan sensor device")
        if not await super(DukaSmartfanTemperature, self).wait_for_device_to_be_ready():
            return False
        _LOGGER.debug("Waiting for dukasmartfan temperature sensor")
        timeout = time.time() + 10
        while self.device is None or self.device.temperature is None:
            if time.time() > timeout:
                _LOGGER.warning("Timeout waiting for temperature reply")
                return False
            await asyncio.sleep(0.1)
        return True

    @property
    def name(self):
        """Return the name"""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id + "_temperature"

    @property
    def should_poll(self):
        """We poll because the fan handle changes."""
        return True

    @property
    def assumed_state(self):
        """Return false if we do optimistic updates."""
        return False

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.device.temperature

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity"""
        return "°C"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:thermometer"

    @property
    def device_info(self):
        return self.dukasmartfan_device_info()
