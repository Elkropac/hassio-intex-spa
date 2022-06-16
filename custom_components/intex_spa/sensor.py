
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

import json
import logging
_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN
from .const import DOMAIN, DATA_CLIENT, DATA_COORDINATOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Setup the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities([SpaCurrentTemperature(coordinator)], True)
    async_add_entities([SpaPresetTemperature(coordinator)], True)


class SpaCurrentTemperature(CoordinatorEntity):
    """Representation of a sensor."""

    _attr_name = "SPA current temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        #self.attrs = {}
        self._state = 0

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "°C"

    @property
    def state(self):
        """Return the state of the sensor."""

        return self.coordinator.data.current_temp

    #@property
    #def extra_state_attributes(self):
    #    return self.attrs

class SpaPresetTemperature(CoordinatorEntity):
    """Representation of a sensor."""

    _attr_name = "SPA preset temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        #self.attrs = {}
        self._state = 0

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "°C"

    @property
    def state(self):
        """Return the state of the sensor."""

        return self.coordinator.data.preset_temp
