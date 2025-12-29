"""Config flow for Zyxel GS1920."""
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from pysnmp.hlapi.asyncio import UsmUserData
from pysnmp.hlapi.usm import usmHMACMD5AuthProtocol, usmAesCfb128Protocol

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input["host"]
            username = user_input["username"]
            auth_key = user_input.get("auth_key")
            priv_key = user_input.get("priv_key")

            user_data = UsmUserData(
                username=username,
                authKey=auth_key,
                privKey=priv_key,
                authProtocol=usmHMACMD5AuthProtocol,
                privProtocol=usmAesCfb128Protocol
            )

            # Kein SNMP-Test beim Import – nur hier asynchron prüfen (optional)
            # ports = await get_ports(host, user_data)

            return self.async_create_entry(title=host, data=user_input)

        data_schema = {
            "host": str,
            "username": str,
            "auth_key": str,
            "priv_key": str
        }

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
