from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta
from .snmp import get_ports, get_poe_status
from pysnmp.hlapi.asyncio import UsmUserData, usmHMACMD5AuthProtocol, usmAesCfb128Protocol

class ZyxelCoordinator(DataUpdateCoordinator):
    """Coordinator for Zyxel GS1920."""

    def __init__(self, hass, host, username, auth_key=None, priv_key=None):
        self._host = host
        self._user_data = UsmUserData(
            username,
            authKey=auth_key,
            privKey=priv_key,
            authProtocol=usmHMACMD5AuthProtocol,
            privProtocol=usmAesCfb128Protocol
        )
        super().__init__(
            hass,
            _LOGGER := None,
            name="Zyxel GS1920",
            update_interval=timedelta(seconds=60),
        )
        self.ports = []

    async def _async_update_data(self):
        self.ports = await get_ports(self._host, self._user_data)
        for port in self.ports:
            port["poe_status"] = await get_poe_status(self._host, self._user_data, port["index"])
        return self.ports
