# sensor.py
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from .snmp import get_ports, get_poe_status
from pysnmp.hlapi.asyncio import UsmUserData, usmHMACMD5AuthProtocol, usmAesCfb128Protocol

async def async_setup_entry(hass, entry, async_add_entities):
    """Sensoren für alle PoE-Ports erstellen."""
    host = entry.data["host"]
    username = entry.data["username"]
    auth_key = entry.data.get("auth_key")
    priv_key = entry.data.get("priv_key")

    user_data = UsmUserData(
        username,
        authKey=auth_key,
        privKey=priv_key,
        authProtocol=usmHMACMD5AuthProtocol,
        privProtocol=usmAesCfb128Protocol
    )

    ports = await get_ports(host, user_data)
    sensors = [ZyxelPoESensor(host, user_data, port["index"], port["name"]) for port in ports]
    async_add_entities(sensors)

class ZyxelPoESensor(Entity):
    """PoE Status Sensor pro Port."""

    def __init__(self, host, user_data, port_index, name):
        self._host = host
        self._user_data = user_data
        self._port_index = port_index
        self._name = name
        self._state = None

    @property
    def name(self):
        return f"{self._name} PoE"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        self._state = await get_poe_status(self._host, self._user_data, self._port_index)
