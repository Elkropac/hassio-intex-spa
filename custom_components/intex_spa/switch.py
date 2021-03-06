
import logging
from typing import Any

from homeassistant.components.switch import (
    DEVICE_CLASS_SWITCH,
    SwitchEntity
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
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
    """Setup the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    spa = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    info = entry.data['info']

    async_add_entities([SpaPowerSwitch(coordinator, spa, info)], True)
    async_add_entities([SpaFilterSwitch(coordinator, spa, info)], True)
    async_add_entities([SpaHeaterSwitch(coordinator, spa, info)], True)
    async_add_entities([SpaBubblesSwitch(coordinator, spa, info)], True)


class SpaPowerSwitch(IntexSpaEntity, SwitchEntity):
    """Representation of a sensor."""

    _attr_name = "SPA power switch"
    _attr_device_class = DEVICE_CLASS_SWITCH

    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        self._attr_unique_id = f"{self.info['unique_id']}_power_switch"
        #self._attr_is_on = self.coordinator.data.power

    @property
    def is_on(self) -> bool:
        """Return state of switch"""
        return self.coordinator.data.power

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch"""
        status = (await self.spa.async_set_power(False))
        self.coordinator.async_set_updated_data(status)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch"""
        status = (await self.spa.async_set_power(True))
        self.coordinator.async_set_updated_data(status)

class SpaFilterSwitch(IntexSpaEntity, SwitchEntity):
    """Representation of a sensor."""

    _attr_name = "SPA filter switch"
    _attr_device_class = DEVICE_CLASS_SWITCH

    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        #self.attrs = {}
        self._attr_unique_id = f"{self.info['unique_id']}_filter_switch"
        self._state = 0

    @property
    def is_on(self) -> bool:
        """Return state of switch"""
        return self.coordinator.data.filter

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch"""
        status = await self.spa.async_set_filter(False)
        self.coordinator.async_set_updated_data(status)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch"""
        status = await self.spa.async_set_filter(True)
        self.coordinator.async_set_updated_data(status)

class SpaHeaterSwitch(IntexSpaEntity, SwitchEntity):
    """Representation of a sensor."""

    _attr_name = "SPA heater switch"
    _attr_device_class = DEVICE_CLASS_SWITCH

    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        self._attr_unique_id = f"{self.info['unique_id']}_heater_switch"
        self._state = 0

    @property
    def is_on(self) -> bool:
        """Return state of switch"""
        return self.coordinator.data.heater

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch"""
        status = await self.spa.async_set_heater(False)
        self.coordinator.async_set_updated_data(status)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch"""
        status = await self.spa.async_set_heater(True)
        self.coordinator.async_set_updated_data(status)

class SpaBubblesSwitch(IntexSpaEntity, SwitchEntity):
    """Representation of a sensor."""

    _attr_name = "SPA bubbles switch"
    _attr_device_class = DEVICE_CLASS_SWITCH

    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        self._attr_unique_id = f"{self.info['unique_id']}_bubbles_switch"
        self._state = 0

    @property
    def is_on(self) -> bool:
        """Return state of switch"""
        return self.coordinator.data.bubbles

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch"""
        status = await self.spa.async_set_bubbles(False)
        self.coordinator.async_set_updated_data(status)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch"""
        status = await self.spa.async_set_bubbles(True)
        self.coordinator.async_set_updated_data(status)