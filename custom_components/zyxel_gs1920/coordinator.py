from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN


class ZyxelGS1920Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, snmp_client):
        super().__init__(
            hass,
            logger=None,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.snmp = snmp_client

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(
                self.snmp.fetch_ports
            )
        except Exception as err:
            raise UpdateFailed(err) from err
