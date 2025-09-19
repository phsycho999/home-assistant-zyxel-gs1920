"""Config flow for Zyxel GS1920 integration."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("username"): str,
                    vol.Required("auth_key"): str,
                    vol.Required("priv_key"): str,
                    vol.Optional("port", default=161): int,
                })
            )

        # Dynamischer Import, um Blocking Warning zu vermeiden
        from .snmp import test_snmpv3_connection

        ok, msg = await test_snmpv3_connection(
            user_input["host"],
            user_input["username"],
            user_input["auth_key"],
            user_input["priv_key"],
            user_input.get("port", 161),
        )

        if not ok:
            errors["base"] = "cannot_connect"
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("username"): str,
                    vol.Required("auth_key"): str,
                    vol.Required("priv_key"): str,
                    vol.Optional("port", default=161): int,
                }),
                errors=errors,
            )

        return self.async_create_entry(
            title=user_input["host"],
            data=user_input
        )
