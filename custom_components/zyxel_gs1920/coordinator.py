from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from .snmp import ZyxelSNMP

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

class ZyxelCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data retrieval."""

    def __init__(self, hass, entry):
        self.entry = entry
        self.snmp = ZyxelSNMP(
            host=entry.data[CONF_HOST],
            username=entry.data[CONF_USERNAME],
            auth_key=entry.data[CONF_PASSWORD]
        )

        super().__init__(
            hass,
            _LOGGER:=hass.logger,
            name="zyxel_gs1920",
            update_interval=timedelta(seconds=30)
        )

    async def _async_update_data(self):
        try:
            return await self.snmp.get_port_status()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")
