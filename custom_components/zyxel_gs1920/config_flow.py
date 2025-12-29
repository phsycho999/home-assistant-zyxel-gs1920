from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("username"): str,
        vol.Optional("auth_key", default=""): str,
        vol.Optional("priv_key", default=""): str,
    }
)

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

        return self.async_create_entry(title=f"Zyxel GS1920 {user_input['host']}", data=user_input)
