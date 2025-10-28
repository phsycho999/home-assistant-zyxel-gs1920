import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_SNMP_PORT, DEFAULT_COMMUNITY

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input["host"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Optional("community", default=DEFAULT_COMMUNITY): str,
            vol.Optional("port", default=DEFAULT_SNMP_PORT): int,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
