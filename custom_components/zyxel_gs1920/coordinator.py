from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .snmp import ZyxelSNMPClient


class ZyxelGS1920Coordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry):
        self.snmp = ZyxelSNMPClient(
            host=entry.data["host"],
            username=entry.data["username"],
            auth_key=entry.data["auth_key"],
            priv_key=entry.data["priv_key"],
        )

        super().__init__(
            hass,
            logger=None,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        return await self.snmp.get_ports()
