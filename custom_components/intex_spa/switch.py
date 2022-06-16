
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from intex_spa.intex_spa import IntexSpa

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
    spa = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    async_add_entities([SpaPowerSwitch(coordinator, spa)], True)
    async_add_entities([SpaFilterSwitch(coordinator, spa)], True)
    async_add_entities([SpaHeaterSwitch(coordinator, spa)], True)
    async_add_entities([SpaBubblesSwitch(coordinator, spa)], True)


class SpaPowerSwitch(CoordinatorEntity):
    """Representation of a sensor."""

    _attr_name = "SPA power switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa):
        super().__init__(coordinator)
        self.spa = spa
        #self.attrs = {}
        self._state = 0

    @property
    def should_pool(self):
        return False

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.power)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_power(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_power(True)

class SpaFilterSwitch(CoordinatorEntity):
    """Representation of a sensor."""

    _attr_name = "SPA filter switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa):
        super().__init__(coordinator)
        self.spa = spa
        #self.attrs = {}
        self._state = 0

    @property
    def should_pool(self):
        return False

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.filter)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_filter(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_filter(True)

class SpaHeaterSwitch(CoordinatorEntity):
    """Representation of a sensor."""

    _attr_name = "SPA heater switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa):
        super().__init__(coordinator)
        self.spa = spa
        #self.attrs = {}
        self._state = 0

    @property
    def should_pool(self):
        return False

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.heater)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_heater(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_heater(True)

class SpaBubblesSwitch(CoordinatorEntity):
    """Representation of a sensor."""

    _attr_name = "SPA bubbles switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa):
        super().__init__(coordinator)
        self.spa = spa
        #self.attrs = {}
        self._state = 0

    @property
    def should_pool(self):
        return False

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.bubble)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_bubbles(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_bubbles(True)
