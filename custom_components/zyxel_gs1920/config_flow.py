from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN


class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Zyxel GS1920 Config Flow"""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["host"],
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Required("auth_key"): str,
                vol.Required("priv_key"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )
