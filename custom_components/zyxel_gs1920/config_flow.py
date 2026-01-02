import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_SNMP_USER, CONF_SNMP_AUTH_KEY, CONF_SNMP_AUTH_PROTO, CONF_SNMP_PRIV_KEY, CONF_SNMP_PRIV_PROTO

class ZyxelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # hier könntest du SNMP Test machen, später
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_SNMP_USER): str,
            vol.Required(CONF_SNMP_AUTH_KEY): str,
            vol.Required(CONF_SNMP_AUTH_PROTO, default="MD5"): vol.In(["MD5", "SHA"]),
            vol.Optional(CONF_SNMP_PRIV_KEY): str,
            vol.Optional(CONF_SNMP_PRIV_PROTO, default="DES"): vol.In(["DES", "AES"]),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
