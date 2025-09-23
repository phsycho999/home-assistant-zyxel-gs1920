"""Config flow for Zyxel GS1920 integration."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
from .snmp import test_snmpv3_connection

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("username"): str,
                    vol.Required("auth_key"): str,
                    vol.Required("priv_key"): str,
                })
            )

        # Test SNMPv3 Verbindung
        valid = await test_snmpv3_connection(user_input)
        if not valid:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("username"): str,
                    vol.Required("auth_key"): str,
                    vol.Required("priv_key"): str,
                }),
                errors={"base": "cannot_connect"}
            )

        return self.async_create_entry(
            title=user_input["host"],
            data=user_input
        )
