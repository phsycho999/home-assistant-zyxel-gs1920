from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Sensoren für alle PoE-Ports dynamisch erstellen."""
    host = entry.data["host"]
    username = entry.data["username"]

    # Lazy Import von pysnmp
    from .snmp import get_ports, get_poe_status
    from pysnmp.hlapi.asyncio import UsmUserData
    from pysnmp.hlapi import usmHMACMD5AuthProtocol, usmAesCfb128Protocol

    user_data = UsmUserData(
        username,
        authKey=None,
        privKey=None,
        authProtocol=usmHMACMD5AuthProtocol,
        privProtocol=usmAesCfb128Protocol
    )

    ports = await get_ports(host, user_data)
    sensors = [ZyxelPoESensor(host, user_data, port["index"], port["name"]) for port in ports]

    async_add_entities(sensors)


class ZyxelPoESensor(Entity):
    def __init__(self, host, user_data, port_index, name):
        self._host = host
        self._user_data = user_data
        self._port_index = port_index
        self._state = None
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        from .snmp import get_poe_status
        self._state = await get_poe_status(self._host, self._user_data, self._port_index)
