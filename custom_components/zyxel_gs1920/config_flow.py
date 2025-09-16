"""Config flow for Zyxel GS1920 integration with SNMPv3 support."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Zyxel GS1920."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is None:
            schema = vol.Schema({
                vol.Required("host"): str,
                vol.Required("snmp_user"): str,
                vol.Required("auth_protocol", default="SHA"): vol.In(["SHA", "MD5"]),
                vol.Required("auth_password"): str,
                vol.Required("priv_protocol", default="AES"): vol.In(["AES", "DES"]),
                vol.Required("priv_password"): str,
            })
            return self.async_show_form(step_id="user", data_schema=schema)

        # Import innerhalb der Funktion → verhindert Blocking-Warnung
        from .snmp import test_snmpv3_connection

        try:
            connection_ok = await test_snmpv3_connection(user_input)
        except Exception as e:
            # Zeigt die genaue Exception in HA
            return self.async_show_form(
                step_id="user",
                data_schema=None,
                errors={"base": f"exception: {e}"}
            )

        if not connection_ok:
            # Prüfe, ob Timeout oder Auth-Problem
            return self.async_show_form(
                step_id="user",
                data_schema=None,
                errors={"base": "SNMPv3 connection failed (check user, auth/priv passwords and algorithms)"}
            )

        return self.async_create_entry(
            title=user_input["host"],
            data=user_input
        )
