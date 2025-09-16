"""Config flow for Zyxel GS1920 integration."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("community"): str,
                })
            )

        return self.async_create_entry(
            title=user_input["host"],
            data=user_input
        )
