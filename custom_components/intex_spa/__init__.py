"""The Intex SPA integration."""
from __future__ import annotations

from intex_spa.intex_spa import IntexSpa

import logging
_LOGGER = logging.getLogger(__name__)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import ATTR_MANUFACTURER, DOMAIN, DATA_CLIENT, DATA_COORDINATOR

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[str] = ["sensor", "switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Intex SPA from a config entry."""

    spa = IntexSpa(entry.data["host"])

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=spa.async_update_status,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=60,
    )
    await coordinator.async_refresh()


    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        DATA_CLIENT: spa,
        DATA_COORDINATOR: coordinator
     
    }

    device_registry = await hass.helpers.device_registry.async_get_registry()
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={('uid', entry.data['info']['uid'])},
        manufacturer=ATTR_MANUFACTURER,
        model=entry.data['info']['model'],
        name=ATTR_MANUFACTURER+" "+entry.data['info']['model']
    )

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
