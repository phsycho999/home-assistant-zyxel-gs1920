from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol

DATA_SCHEMA = vol.Schema({
    vol.Required("host"): str,
    vol.Required("username"): str,
    vol.Optional("authKey"): str,
    vol.Optional("privKey"): str,
})

class ZyxelGS1920FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["host"], data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
