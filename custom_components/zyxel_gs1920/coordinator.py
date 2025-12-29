from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from .snmp import get_ports, get_poe_status

class ZyxelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, user_data):
        super().__init__(
            hass,
            _LOGGER := hass.logger,
            name="Zyxel GS1920",
            update_interval=timedelta(seconds=60),
        )
        self.host = host
        self.user_data = user_data
        self.ports = []

    async def _async_update_data(self):
        try:
            self.ports = await get_ports(self.host, self.user_data)
            for port in self.ports:
                port["poe"] = await get_poe_status(self.host, self.user_data, port["index"])
            return self.ports
        except Exception as e:
            raise UpdateFailed(e)
