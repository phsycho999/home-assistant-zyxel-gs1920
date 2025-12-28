import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

from pysnmp.hlapi.asyncio import UsmUserData, usmHMACMD5AuthProtocol, usmHMACSHAAuthProtocol, usmDESPrivProtocol, usmAesCfb128Protocol

AUTH_PROTOCOLS = {
    "MD5": usmHMACMD5AuthProtocol,
    "SHA": usmHMACSHAAuthProtocol
}

PRIV_PROTOCOLS = {
    "DES": usmDESPrivProtocol,
    "AES": usmAesCfb128Protocol
}

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Versuche, den Switch zu erreichen
            host = user_input["host"]
            username = user_input["username"]
            password = user_input.get("password")
            auth_proto = AUTH_PROTOCOLS[user_input["auth_protocol"]]
            priv_proto = PRIV_PROTOCOLS.get(user_input.get("priv_protocol"))
            priv_key = user_input.get("priv_key")

            user_data = UsmUserData(
                username,
                authKey=password,
                privKey=priv_key,
                authProtocol=auth_proto,
                privProtocol=priv_proto
            )

            # Teste Verbindung über SNMP
            try:
                from .snmp import get_ports
                ports = await get_ports(host, user_data)
                if not ports:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=f"Zyxel GS1920 {host}",
                        data=user_input
                    )
            except Exception as e:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Optional("password"): str,
            vol.Optional("auth_protocol", default="MD5"): vol.In(list(AUTH_PROTOCOLS.keys())),
            vol.Optional("priv_protocol"): vol.In(list(PRIV_PROTOCOLS.keys())),
            vol.Optional("priv_key"): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
