import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_SNMP_PORT
from .snmp import create_user_data, get_ports

class ZyxelGS1920ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            host = user_input["host"]
            username = user_input["username"]
            auth_key = user_input.get("auth_key")
            priv_key = user_input.get("priv_key")

            user_data = create_user_data(username, auth_key, priv_key)
            try:
                ports = await get_ports(host, user_data)
                if not ports:
                    errors["base"] = "no_ports"
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(
                    title=f"Zyxel GS1920 ({host})",
                    data={
                        "host": host,
                        "username": username,
                        "auth_key": auth_key,
                        "priv_key": priv_key,
                        "snmp_port": DEFAULT_SNMP_PORT,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Optional("auth_key"): str,
                vol.Optional("priv_key"): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
