from homeassistant.helpers.entity import ToggleEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """PoE-Schalter für alle Ports dynamisch erstellen."""
    host = entry.data["host"]
    username = entry.data["username"]

    # Lazy Import
    from .snmp import get_ports, set_poe_port
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
    switches = [ZyxelPoESwitch(host, user_data, port["index"], port["name"], set_poe_port) for port in ports]

    async_add_entities(switches)


class ZyxelPoESwitch(ToggleEntity):
    def __init__(self, host, user_data, port_index, name, set_func):
        self._host = host
        self._user_data = user_data
        self._port_index = port_index
        self._name = name
        self._is_on = None
        self._set_func = set_func

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = await self._set_func(self._host, self._user_data, self._port_index, True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = not await self._set_func(self._host, self._user_data, self._port_index, False)
        self.async_write_ha_state()
