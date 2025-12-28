from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .snmp import get_ports, get_poe_status

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Zyxel GS1920 from a config entry."""
    host = entry.data["host"]
    username = entry.data["username"]
    password = entry.data.get("password")
    auth_protocol = entry.data.get("auth_protocol")
    priv_protocol = entry.data.get("priv_protocol")
    priv_key = entry.data.get("priv_key")
    
    from pysnmp.hlapi.asyncio import UsmUserData, usmHMACMD5AuthProtocol, usmAesCfb128Protocol
    
    user_data = UsmUserData(
        username,
        authKey=password,
        privKey=priv_key,
        authProtocol=auth_protocol or usmHMACMD5AuthProtocol,
        privProtocol=priv_protocol or usmAesCfb128Protocol
    )

    coordinator = ZyxelCoordinator(hass, host, user_data)
    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, ["sensor", "switch"])

    return True


class ZyxelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, user_data):
        super().__init__(
            hass,
            _LOGGER := None,
            name="Zyxel GS1920 Coordinator",
            update_interval=None
        )
        self.host = host
        self.user_data = user_data
        self.data = {}

    async def _async_update_data(self):
        """Fetch ports and PoE status."""
        ports = await get_ports(self.host, self.user_data)
        data = {}
        for port in ports:
            poe = await get_poe_status(self.host, self.user_data, port["index"])
            data[port["index"]] = {
                "name": port["name"],
                "poe": poe
            }
        self.data = data
        return self.data
