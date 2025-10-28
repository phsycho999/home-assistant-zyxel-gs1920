import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_COMMUNITY, CONF_SNMP_VERSION, CONF_USER, CONF_AUTH_KEY, CONF_PRIV_KEY

SNMP_VERSIONS = ["1", "2c", "3"]

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Daten aus User Input speichern
            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data={
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_SNMP_VERSION: user_input[CONF_SNMP_VERSION],
                    CONF_COMMUNITY: user_input.get(CONF_COMMUNITY, ""),
                    CONF_USER: user_input.get(CONF_USER, ""),
                    CONF_AUTH_KEY: user_input.get(CONF_AUTH_KEY, ""),
                    CONF_PRIV_KEY: user_input.get(CONF_PRIV_KEY, "")
                }
            )

        # Formular für die UI
        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_SNMP_VERSION, default="2c"): vol.In(SNMP_VERSIONS),
            vol.Optional(CONF_COMMUNITY, default="public"): str,
            vol.Optional(CONF_USER, default=""): str,
            vol.Optional(CONF_AUTH_KEY, default=""): str,
            vol.Optional(CONF_PRIV_KEY, default=""): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
