from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .snmp import get_ports, get_poe_status, build_user
from .const import DOMAIN


class ZyxelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config):
        self.host = config["host"]
        self.user = build_user(
            config["username"],
            config["auth_key"],
            config["priv_key"],
        )

        super().__init__(
            hass,
            logger=None,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        ports = await get_ports(self.host, self.user)
        data = {}

        for idx, name in ports.items():
            poe = await get_poe_status(self.host, self.user, idx)
            data[idx] = {
                "name": name,
                "poe": poe,
            }

        return data
