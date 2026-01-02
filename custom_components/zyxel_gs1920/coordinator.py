from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from .snmp import ZyxelSNMP
from .const import CONF_HOST, CONF_USERNAME, CONF_AUTH_KEY, CONF_PRIV_KEY, CONF_SECURITY_LEVEL

class ZyxelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.snmp = ZyxelSNMP(
            host=entry.data[CONF_HOST],
            username=entry.data[CONF_USERNAME],
            auth_key=entry.data[CONF_AUTH_KEY],
            priv_key=entry.data[CONF_PRIV_KEY],
            security_level=entry.data[CONF_SECURITY_LEVEL],
        )

        super().__init__(
            hass,
            _LOGGER,
            name="Zyxel GS1920",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        try:
            # Beispiel OID: System Name
            system_name = await self.snmp.get("1.3.6.1.2.1.1.5.0")
            return {"system_name": str(system_name)}
        except Exception as e:
            raise UpdateFailed(e)
