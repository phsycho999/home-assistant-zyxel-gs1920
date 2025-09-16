"""Config flow for Zyxel GS1920 integration with SNMPv3 support."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
from .snmp import test_snmpv3_connection

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Zyxel GS1920 with SNMPv3."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is None:
            # Formular für SNMPv3-Parameter
            schema = vol.Schema({
                vol.Required("host"): str,
                vol.Required("snmp_user"): str,
                vol.Required("auth_protocol", default="SHA"): vol.In(["SHA", "MD5"]),
                vol.Required("auth_password"): str,
                vol.Required("priv_protocol", default="AES"): vol.In(["AES", "DES"]),
                vol.Required("priv_password"): str,
            })
            return self.async_show_form(step_id="user", data_schema=schema)

        # Verbindungstest vor dem Speichern
        if not await test_snmpv3_connection(user_input):
            return self.async_show_form(
                step_id="user",
                data_schema=None,
                errors={"base": "connection_failed"}
            )

        # Erfolgreich → Integrationseintrag erstellen
        return self.async_create_entry(
            title=user_input["host"],
            data=user_input
        )
