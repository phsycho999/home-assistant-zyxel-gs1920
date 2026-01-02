from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_USERNAME,
    CONF_AUTH_KEY,
    CONF_PRIV_KEY,
)
from .snmp import snmp_test_connection


class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                await self.hass.async_add_executor_job(
                    snmp_test_connection,
                    user_input[CONF_HOST],
                    user_input[CONF_USERNAME],
                    user_input[CONF_AUTH_KEY],
                    user_input[CONF_PRIV_KEY],
                )
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Zyxel GS1920 ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_AUTH_KEY): str,
                vol.Required(CONF_PRIV_KEY): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
