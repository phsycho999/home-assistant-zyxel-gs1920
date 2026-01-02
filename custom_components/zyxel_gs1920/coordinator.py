import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .snmp import ZyxelSNMP
from .const import CONF_HOST, CONF_SNMP_USER, CONF_SNMP_AUTH_KEY, CONF_SNMP_AUTH_PROTO, CONF_SNMP_PRIV_KEY, CONF_SNMP_PRIV_PROTO

_LOGGER = logging.getLogger(__name__)

class ZyxelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            _LOGGER,
            name=f"Zyxel GS1920 {entry.data[CONF_HOST]}",
            update_interval=30,
        )

        self.snmp = ZyxelSNMP(
            host=entry.data[CONF_HOST],
            user=entry.data[CONF_SNMP_USER],
            auth_key=entry.data[CONF_SNMP_AUTH_KEY],
            auth_proto=entry.data[CONF_SNMP_AUTH_PROTO],
            priv_key=entry.data.get(CONF_SNMP_PRIV_KEY),
            priv_proto=entry.data.get(CONF_SNMP_PRIV_PROTO),
        )

    async def _async_update_data(self):
        """Fetch data from the switch via SNMP."""
        return await self.snmp.get_system_name()
