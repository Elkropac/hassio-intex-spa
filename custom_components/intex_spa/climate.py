
import logging

from homeassistant.components.climate import (
    ClimateEntity,
)
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from intex_spa.intex_spa import IntexSpa

from .const import DOMAIN, DATA_CLIENT, DATA_COORDINATOR
from .model import IntexSpaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Setup the climate platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    spa = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    info = entry.data['info']

    async_add_entities([SpaClimate(coordinator, spa, info)], True)


class SpaClimate(IntexSpaEntity, ClimateEntity):
    """Representation of a climate."""

    _attr_name = "SPA climate"
    _attr_hvac_modes = [
        HVAC_MODE_HEAT,
        HVAC_MODE_OFF,
    ]
    _attr_max_temp = 40
    _attr_min_temp = 20
    _attr_supported_features = (SUPPORT_TARGET_TEMPERATURE)
    _attr_target_temperature_step = 1
    _attr_temperature_unit = TEMP_CELSIUS

    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info

        self._attr_unique_id = f"{self.info['unique_id']}_climate"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the state of the sensor."""
        return self.coordinator.data.current_temp

    @property
    def target_temperature(self):
        """Return the state of the sensor."""
        return self.coordinator.data.preset_temp

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        status = await self.spa.async_set_preset_temp(int(kwargs.get(ATTR_TEMPERATURE)))
        self.coordinator.async_set_updated_data(status)

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, off"""
        if self.coordinator.data.power:
            return HVAC_MODE_HEAT

        return HVAC_MODE_OFF

    async def async_set_hvac_mode(self, hvac_mode):
        """Set HVAC mode."""
        if hvac_mode == HVAC_MODE_OFF:
            status = await self.spa.async_set_power(False)
            self.coordinator.async_set_updated_data(status)
            return

        if hvac_mode == HVAC_MODE_HEAT:
            status = await self.spa.async_set_power(True)
            self.coordinator.async_set_updated_data(status)
            return
    