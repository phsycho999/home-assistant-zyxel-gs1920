from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .snmp import snmp_get_sysdescr

_LOGGER = logging.getLogger(__name__)


class ZyxelGS1920Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

        self.host = entry.data["host"]
        self.username = entry.data["username"]
        self.auth_key = entry.data["auth_key"]
        self.priv_key = entry.data["priv_key"]

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.host}",
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        try:
            # SNMP läuft BLOCKING → sauber in Executor
            return await self.hass.async_add_executor_job(
                snmp_get_sysdescr,
                self.host,
                self.username,
                self.auth_key,
                self.priv_key,
            )
        except Exception as err:
            raise UpdateFailed(f"SNMP update failed: {err}") from err
