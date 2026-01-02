import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST

DOMAIN = "zyxel_gs1920"

CONF_SNMP_USER = "snmp_user"
CONF_SNMP_AUTH_KEY = "snmp_auth_key"
CONF_SNMP_AUTH_PROTO = "snmp_auth_proto"
CONF_SNMP_PRIV_KEY = "snmp_priv_key"
CONF_SNMP_PRIV_PROTO = "snmp_priv_proto"

AUTH_PROTOCOLS = ["MD5", "SHA"]
PRIV_PROTOCOLS = ["DES", "AES"]

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Zyxel GS1920 SNMPv3."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Daten als entry speichern
            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_SNMP_USER): str,
            vol.Required(CONF_SNMP_AUTH_KEY): str,
            vol.Required(CONF_SNMP_AUTH_PROTO, default="MD5"): vol.In(AUTH_PROTOCOLS),
            vol.Required(CONF_SNMP_PRIV_KEY, default=""): str,
            vol.Required(CONF_SNMP_PRIV_PROTO, default="DES"): vol.In(PRIV_PROTOCOLS),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
