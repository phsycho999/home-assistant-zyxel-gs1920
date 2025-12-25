from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_HOST, CONF_USER, CONF_AUTH_KEY, CONF_PRIV_KEY, CONF_SNMP_VERSION

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Zyxel GS1920 (SNMPv3 only)."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_HOST, description={"suggested_value": "192.168.1.1"}): str,
            vol.Required(CONF_SNMP_VERSION, default="3"): str,
            vol.Required(CONF_USER, description={"suggested_value": "snmpuser"}): str,
            vol.Required(CONF_AUTH_KEY, description={"suggested_value": "authpass"}): str,
            vol.Optional(CONF_PRIV_KEY, description={"suggested_value": "privpass"}): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
