import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_COMMUNITY

DEFAULT_SNMP_PORT = 161
DEFAULT_COMMUNITY = "public"

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain="zyxel_gs1920"):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data={
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_PORT: user_input.get(CONF_PORT, DEFAULT_SNMP_PORT),
                    CONF_COMMUNITY: user_input.get(CONF_COMMUNITY, DEFAULT_COMMUNITY),
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default=DEFAULT_SNMP_PORT): int,
                vol.Optional(CONF_COMMUNITY, default=DEFAULT_COMMUNITY): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
