import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

SNMP_VERSIONS = ["2c", "3"]

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zyxel GS1920 switch."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Step when the user initializes the flow."""
        errors = {}

        if user_input is not None:
            # Validate input here if needed
            return self.async_create_entry(title=user_input["host"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("snmp_version", default="2c"): vol.In(SNMP_VERSIONS),
            vol.Optional("community", default="public"): str,
            vol.Optional("username"): str,
            vol.Optional("auth_protocol"): vol.In(["MD5", "SHA", "None"]),
            vol.Optional("auth_key"): str,
            vol.Optional("priv_protocol"): vol.In(["DES", "AES", "None"]),
            vol.Optional("priv_key"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
