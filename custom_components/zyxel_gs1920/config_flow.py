import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_AUTH_KEY, CONF_PRIV_KEY, CONF_SECURITY_LEVEL, SECURITY_LEVELS

class ZyxelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_AUTH_KEY): str,
                vol.Required(CONF_PRIV_KEY): str,
                vol.Required(CONF_SECURITY_LEVEL, default="authPriv"): vol.In(SECURITY_LEVELS),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)
