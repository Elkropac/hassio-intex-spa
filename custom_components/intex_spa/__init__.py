"""The Intex SPA integration."""
from __future__ import annotations

from .spa import Spa

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
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    _LOGGER.error(entry.data["host"])
    #hass.data[DOMAIN][entry.entry_id] = Telnet(entry.data["host"], entry.data["port"])

    spa = Spa(entry.data["host"], entry.data["port"])

    try:
        info = await spa.connect()
    except Exception as e:
        return False

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=spa.get_update,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=60,
    )


    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        DATA_CLIENT: spa,
        DATA_COORDINATOR: coordinator
     
    }

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
