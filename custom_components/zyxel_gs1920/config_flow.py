import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN

CONF_SNMP_VERSION = "snmp_version"
CONF_COMMUNITY = "community"
CONF_AUTH_PROTOCOL = "auth_protocol"
CONF_PRIV_PROTOCOL = "priv_protocol"
CONF_AUTH_KEY = "auth_key"
CONF_PRIV_KEY = "priv_key"

SNMP_VERSIONS = ["2c", "3"]
AUTH_PROTOCOLS = ["MD5", "SHA"]
PRIV_PROTOCOLS = ["DES", "AES"]

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zyxel GS1920."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            self.snmp_version = user_input[CONF_SNMP_VERSION]

            if self.snmp_version == "2c":
                return await self.async_step_snmp2c()
            else:
                return await self.async_step_snmp3()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_SNMP_VERSION, default="2c"): vol.In(SNMP_VERSIONS),
            })
        )

    async def async_step_snmp2c(self, user_input=None):
        """SNMP v2c step."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data={
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_SNMP_VERSION: "2c",
                    CONF_COMMUNITY: user_input.get(CONF_COMMUNITY, "public")
                }
            )

        return self.async_show_form(
            step_id="snmp2c",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_COMMUNITY, default="public"): str,
            })
        )

    async def async_step_snmp3(self, user_input=None):
        """SNMP v3 step."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data={
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_SNMP_VERSION: "3",
                    CONF_USERNAME: user_input[CONF_USERNAME],
                    CONF_AUTH_PROTOCOL: user_input[CONF_AUTH_PROTOCOL],
                    CONF_AUTH_KEY: user_input[CONF_AUTH_KEY],
                    CONF_PRIV_PROTOCOL: user_input[CONF_PRIV_PROTOCOL],
                    CONF_PRIV_KEY: user_input[CONF_PRIV_KEY],
                }
            )

        return self.async_show_form(
            step_id="snmp3",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_AUTH_PROTOCOL, default="MD5"): vol.In(AUTH_PROTOCOLS),
                vol.Required(CONF_AUTH_KEY): str,
                vol.Required(CONF_PRIV_PROTOCOL, default="DES"): vol.In(PRIV_PROTOCOLS),
                vol.Required(CONF_PRIV_KEY): str,
            })
        )
