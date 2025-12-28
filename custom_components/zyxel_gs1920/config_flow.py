# config_flow.py
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validierung von IP/Benutzername kann hier später ergänzt werden
            return self.async_create_entry(title=user_input["host"], data=user_input)

        schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Optional("auth_key"): str,
            vol.Optional("priv_key"): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
