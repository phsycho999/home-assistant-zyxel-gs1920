from homeassistant import config_entries
from .const import DOMAIN
from pysnmp.hlapi.asyncio import UsmUserData, usmHMACMD5AuthProtocol, usmAesCfb128Protocol

class ZyxelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            self.host = user_input["host"]
            self.username = user_input["username"]
            self.user_data = UsmUserData(
                self.username,
                authKey=None,
                privKey=None,
                authProtocol=usmHMACMD5AuthProtocol,
                privProtocol=usmAesCfb128Protocol
            )
            return self.async_create_entry(title=f"Zyxel {self.host}", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_data_schema(),
            errors=errors
        )

    def _get_data_schema(self):
        import voluptuous as vol
        from homeassistant.helpers import config_validation as cv
        return vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str
        })
