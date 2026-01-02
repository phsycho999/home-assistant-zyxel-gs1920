from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .snmp import ZyxelSNMP
from .const import DOMAIN


class ZyxelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config):
        self.snmp = ZyxelSNMP(
            config["host"],
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
        try:
            # Beispiel: System Name
            sys_name = await self.snmp.get("1.3.6.1.2.1.1.5.0")

            return {
                "sys_name": str(sys_name),
            }

        except Exception as err:
            raise UpdateFailed(err) from err
