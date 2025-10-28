import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from .const import (
    DOMAIN,
    CONF_COMMUNITY,
    CONF_SNMP_VERSION,
    CONF_USER,
    CONF_AUTH_KEY,
    CONF_PRIV_KEY,
)

SNMP_VERSIONS = ["2c", "3"]

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCALPOLL

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input.get(CONF_HOST)
            snmp_version = user_input.get(CONF_SNMP_VERSION)
            community = user_input.get(CONF_COMMUNITY)
            user = user_input.get(CONF_USER)
            auth_key = user_input.get(CONF_AUTH_KEY)
            priv_key = user_input.get(CONF_PRIV_KEY)

            return self.async_create_entry(
                title=host,
                data={
                    CONF_HOST: host,
                    CONF_SNMP_VERSION: snmp_version,
                    CONF_COMMUNITY: community,
                    CONF_USER: user,
                    CONF_AUTH_KEY: auth_key,
                    CONF_PRIV_KEY: priv_key,
                },
            )

        # Form Schema
        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_SNMP_VERSION, default="2c"): vol.In(SNMP_VERSIONS),
            vol.Optional(CONF_COMMUNITY, default="public"): str,
            vol.Optional(CONF_USER, default=""): str,
            vol.Optional(CONF_AUTH_KEY, default=""): str,
            vol.Optional(CONF_PRIV_KEY, default=""): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
