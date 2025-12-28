# switch.py
from homeassistant.helpers.entity import ToggleEntity
from .const import DOMAIN
from .snmp import get_ports, set_poe_port, get_poe_status
from pysnmp.hlapi.asyncio import UsmUserData, usmHMACMD5AuthProtocol, usmAesCfb128Protocol

async def async_setup_entry(hass, entry, async_add_entities):
    """PoE-Schalter für alle Ports erstellen."""
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
    switches = [ZyxelPoESwitch(host, user_data, port["index"], port["name"]) for port in ports]
    async_add_entities(switches)

class ZyxelPoESwitch(ToggleEntity):
    """PoE Schalter pro Port."""

    def __init__(self, host, user_data, port_index, name):
        self._host = host
        self._user_data = user_data
        self._port_index = port_index
        self._name = name
        self._is_on = None

    @property
    def name(self):
        return f"{self._name} PoE"

    @property
    def is_on(self):
        return self._is_on

    async def async_update(self):
        self._is_on = await get_poe_status(self._host, self._user_data, self._port_index)

    async def async_turn_on(self, **kwargs):
        result = await set_poe_port(self._host, self._user_data, self._port_index, True)
        if result:
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        result = await set_poe_port(self._host, self._user_data, self._port_index, False)
        if result:
            self._is_on = False
            self.async_write_ha_state()
