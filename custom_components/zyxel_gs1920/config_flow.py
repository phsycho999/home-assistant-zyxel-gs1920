import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input["host"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Optional("auth_key", default=""): str,
            vol.Optional("priv_key", default=""): str
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
