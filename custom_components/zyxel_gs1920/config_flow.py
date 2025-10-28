"""UI configuration for Zyxel GS1920"""
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_COMMUNITY
import voluptuous as vol

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_COMMUNITY, default="public"): str
})

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain="zyxel_gs1920"):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
