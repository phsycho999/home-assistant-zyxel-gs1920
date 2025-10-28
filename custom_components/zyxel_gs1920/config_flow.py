import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class ZyxelGS1920FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zyxel GS1920."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize the flow."""
        self.host = None
        self.community = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input.get("host")
            community = user_input.get("community", "public")

            # Optional: SNMP Verbindung prüfen hier
            # try:
            #     await test_snmp_connection(host, community)
            # except Exception:
            #     errors["base"] = "cannot_connect"
            # else:
            #     return self.async_create_entry(
            #         title=host,
            #         data={"host": host, "community": community},
            #     )

            # Für einfachen Start einfach anlegen
            return self.async_create_entry(
                title=host,
                data={"host": host, "community": community},
            )

        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Optional("community", default="public"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
