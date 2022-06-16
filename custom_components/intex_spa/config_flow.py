"""Config flow for Intex SPA integration."""
from __future__ import annotations

from .spa import Spa

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import ATTR_MANUFACTURER, DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("port", default=8990): int,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    
    #try:
    #    spa = get_spa(hass, data["host"], data["port"])
    #except (ConnectionResetError):
    #    raise CannotConnect
    #except:
    #    raise Exception
    #info = spa.get_device_info()

    spa = Spa(data["host"], data["port"])
    #info = (await hass.async_add_executor_job(spa.get_device_info))
    info = (await spa.connect())

    _LOGGER.exception(info)

    data['info'] = info
    data['title'] = ATTR_MANUFACTURER + " " + info['model']
    
    #return self.async_create_entry(title=desc, data=data)
    return data



class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Intex SPA."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
            return self.async_create_entry(title=info["title"], data=info)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        
        #if info is not None:
        #    return self.async_create_entry(title=info["title"], data=user_input)

        errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
