"""
Sensor platform for Duka Smartfan fan.

see http://www.dingus.dk for more information
"""

import asyncio
import logging
import time

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_NAME,
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .dukaentity import DukaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Duka Smartfan sensors based on a config entry."""

    name = entry.data[CONF_NAME]
    device_id = entry.data[CONF_DEVICE_ID]
    duka_smartfan_humidity_sensor = DukaSmartfanHumidity(
        hass, name + " humidity", device_id
    )
    duka_smartfan_temperature_sensor = DukaSmartfanTemperature(
        hass, name + " temperature", device_id
    )
    duka_smartfan_fan_speed_sensor = DukaSmartfanFanSpeed(
        hass, name + " fan speed", device_id
    )
    humidity_ready = await duka_smartfan_humidity_sensor.wait_for_device_to_be_ready()
    temperature_ready = (
        await duka_smartfan_temperature_sensor.wait_for_device_to_be_ready()
    )
    fan_speed_ready = await duka_smartfan_fan_speed_sensor.wait_for_device_to_be_ready()
    if not (humidity_ready or temperature_ready or fan_speed_ready):
        _LOGGER.error("Failed to setup dukasmartfan device")
        return
    async_add_entities(
        [
            duka_smartfan_humidity_sensor,
            duka_smartfan_temperature_sensor,
            duka_smartfan_fan_speed_sensor,
        ],
        True,
    )


class DukaSmartfanHumidity(SensorEntity, DukaEntity):
    """A Duka Smartfan humidity sensor entity."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:water-percent"
    _attr_should_poll = True
    _attr_assumed_state = False

    def __init__(self, hass: HomeAssistant, name: str, device_id: str):
        """Initialize the Duka Smartfan humidity sensor."""
        super(DukaSmartfanHumidity, self).__init__(hass, device_id)
        self._attr_name = name

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
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id + "_humidity"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.device is None:
            return None
        return self.device.humidity

    @property
    def device_info(self) -> DeviceInfo | None:
        return self.dukasmartfan_device_info()


class DukaSmartfanTemperature(SensorEntity, DukaEntity):
    """A Duka Smartfan temperature sensor entity."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer"
    _attr_should_poll = True
    _attr_assumed_state = False

    def __init__(self, hass: HomeAssistant, name: str, device_id: str):
        """Initialize the Duka Smartfan temperature sensor."""
        super(DukaSmartfanTemperature, self).__init__(hass, device_id)
        self._attr_name = name

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
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id + "_temperature"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.device is None:
            return None
        return self.device.temperature

    @property
    def device_info(self) -> DeviceInfo | None:
        return self.dukasmartfan_device_info()


class DukaSmartfanFanSpeed(SensorEntity, DukaEntity):
    """A Duka Smartfan fan speed sensor entity."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = REVOLUTIONS_PER_MINUTE
    _attr_icon = "mdi:fan"
    _attr_should_poll = True
    _attr_assumed_state = False

    def __init__(self, hass: HomeAssistant, name: str, device_id: str):
        """Initialize the Duka Smartfan fan speed sensor."""
        super(DukaSmartfanFanSpeed, self).__init__(hass, device_id)
        self._attr_name = name

    async def wait_for_device_to_be_ready(self):
        """Wait for the device to be initialized.

        Then wait until the first fan speed command has been received"""
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
        if not await super(DukaSmartfanFanSpeed, self).wait_for_device_to_be_ready():
            return False
        _LOGGER.debug("Waiting for dukasmartfan fan speed sensor")
        timeout = time.time() + 10
        while self.device is None or self.device.fan_speed is None:
            if time.time() > timeout:
                _LOGGER.warning("Timeout waiting for fan speed reply")
                return False
            await asyncio.sleep(0.1)
        return True

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id + "_fan_speed"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.device is None:
            return None
        return self.device.fan_speed

    @property
    def device_info(self) -> DeviceInfo | None:
        return self.dukasmartfan_device_info()
