import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_COMMUNITY, CONF_SNMP_VERSION, CONF_USER, CONF_AUTH_KEY, CONF_PRIV_KEY

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            schema = vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_SNMP_VERSION, default="2c"): str,
                vol.Optional(CONF_COMMUNITY, default="public"): str,
                vol.Optional(CONF_USER, default=""): str,
                vol.Optional(CONF_AUTH_KEY, default=""): str,
                vol.Optional(CONF_PRIV_KEY, default=""): str,
            })
            return self.async_show_form(step_id="user", data_schema=schema)

        return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)
