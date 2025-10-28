from homeassistant import config_entries
from .const import DOMAIN

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            return self.async_create_entry(title=user_input["host"], data=user_input)

        schema = {
            "host": str,
            "snmp_version": str,
            "community": str,
            "username": str,
            "auth_protocol": str,
            "auth_key": str,
            "priv_protocol": str,
            "priv_key": str
        }
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
