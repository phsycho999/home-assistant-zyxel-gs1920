from homeassistant.helpers.entity import ToggleEntity
from .const import DOMAIN
from .snmp import get_ports, set_poe_port
from pysnmp.hlapi import UsmUserData, usmHMACMD5AuthProtocol, usmAesCfb128Protocol

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    username = entry.data["username"]
    authKey = entry.data.get("authKey")
    privKey = entry.data.get("privKey")

    user_data = UsmUserData(
        username, authKey=authKey, privKey=privKey,
        authProtocol=usmHMACMD5AuthProtocol,
        privProtocol=usmAesCfb128Protocol
    )

    ports = await get_ports(host, user_data)
    switches = [ZyxelPoESwitch(host, user_data, p["index"], p["name"]) for p in ports]
    async_add_entities(switches)

class ZyxelPoESwitch(ToggleEntity):
    def __init__(self, host, user_data, port_index, name):
        self._host = host
        self._user_data = user_data
        self._port_index = port_index
        self._name = name
        self._is_on = None

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = await set_poe_port(self._host, self._user_data, self._port_index, True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = not await set_poe_port(self._host, self._user_data, self._port_index, False)
        self.async_write_ha_state()
