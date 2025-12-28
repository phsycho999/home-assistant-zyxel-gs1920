import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

# Optional: Standardwerte
DEFAULT_SNMP_PORT = 161

class ZyxelGS1920FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zyxel GS1920 switch via SNMPv3."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize the flow."""
        self._host = None
        self._username = None
        self._auth_key = None
        self._priv_key = None

    async def async_step_user(self, user_input=None):
        """Step when user initiates the config flow."""

        if user_input is not None:
            self._host = user_input["host"]
            self._username = user_input["username"]
            self._auth_key = user_input.get("auth_key")
            self._priv_key = user_input.get("priv_key")

            # Optional: Hier könntest du prüfen, ob das Gerät erreichbar ist via SNMP
            return self.async_create_entry(
                title=f"Zyxel GS1920 ({self._host})",
                data={
                    "host": self._host,
                    "username": self._username,
                    "auth_key": self._auth_key,
                    "priv_key": self._priv_key,
                    "port": DEFAULT_SNMP_PORT
                }
            )

        # Formular anzeigen
        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Optional("auth_key", default=""): str,
            vol.Optional("priv_key", default=""): str,
        })
        return self.async_show_form(step_id="user", data_schema=data_schema)
