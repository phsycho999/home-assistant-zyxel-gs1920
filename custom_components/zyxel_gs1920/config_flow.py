"""Config flow for Zyxel GS1920 integration."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
from .snmp import test_snmpv3_connection_sync
import logging

_LOGGER = logging.getLogger(__name__)

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("snmp_user"): str,
                    vol.Required("auth_password"): str,
                    vol.Required("priv_password"): str,
                    vol.Optional("auth_protocol", default="SHA"): str,
                    vol.Optional("priv_protocol", default="AES"): str,
                })
            )

        # Test SNMPv3 connection
        success = await self.hass.async_add_executor_job(
            test_snmpv3_connection_sync, user_input
        )

        if not success:
            _LOGGER.error("SNMPv3 connection failed for host %s", user_input["host"])
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("snmp_user"): str,
                    vol.Required("auth_password"): str,
                    vol.Required("priv_password"): str,
                    vol.Optional("auth_protocol", default="SHA"): str,
                    vol.Optional("priv_protocol", default="AES"): str,
                }),
                errors={"base": "cannot_connect"}
            )

        return self.async_create_entry(
            title=user_input["host"],
            data=user_input
        )
