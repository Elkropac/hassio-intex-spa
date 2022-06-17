
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


class SpaPowerSwitch(IntexSpaEntity):
    """Representation of a sensor."""

    _attr_name = "SPA power switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        self._attr_unique_id = f"{self.info['unique_id']}_power_switch"
        self._state = 0

#    @property
#    def should_pool(self):
#        return False

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.power

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_power(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_power(True)

class SpaFilterSwitch(IntexSpaEntity):
    """Representation of a sensor."""

    _attr_name = "SPA filter switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        #self.attrs = {}
        self._attr_unique_id = f"{self.info['unique_id']}_filter_switch"
        self._state = 0

    @property
    def should_pool(self):
        return False

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.filter

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_filter(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_filter(True)

class SpaHeaterSwitch(IntexSpaEntity):
    """Representation of a sensor."""

    _attr_name = "SPA heater switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        self._attr_unique_id = f"{self.info['unique_id']}_heater_switch"
        self._state = 0

    @property
    def should_pool(self):
        return False

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.heater

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_heater(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_heater(True)

class SpaBubblesSwitch(IntexSpaEntity):
    """Representation of a sensor."""

    _attr_name = "SPA bubbles switch"
    def __init__(self, coordinator: DataUpdateCoordinator, spa: IntexSpa, info):
        super().__init__(coordinator)
        self.spa = spa
        self.info = info
        self._attr_unique_id = f"{self.info['unique_id']}_bubbles_switch"
        self._state = 0

    @property
    def should_pool(self):
        return False

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.bubble

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.spa.async_set_bubbles(False)


    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.spa.async_set_bubbles(True)
