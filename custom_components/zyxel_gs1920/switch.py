from homeassistant.helpers.entity import SwitchEntity
from .snmp import snmp_get, snmp_set

class ZyxelPortSwitch(SwitchEntity):
    """Ein-/Ausschalten eines Ports."""

    def __init__(self, host, community, port_number, oid):
        self._host = host
        self._community = community
        self._port = port_number
        self._oid = oid
        self._state = None

    @property
    def name(self):
        return f"Port {self._port}"

    @property
    def is_on(self):
        return self._state == 1

    async def async_turn_on(self, **kwargs):
        await snmp_set(self._host, self._community, self._oid, 1)
        self._state = 1

    async def async_turn_off(self, **kwargs):
        await snmp_set(self._host, self._community, self._oid, 2)
        self._state = 2

    async def async_update(self):
        value = await snmp_get(self._host, self._community, self._oid)
        self._state = int(value)


class ZyxelPoESwitch(SwitchEntity):
    """Ein-/Ausschalten der PoE-Funktion eines Ports."""

    def __init__(self, host, community, port_number, oid):
        self._host = host
        self._community = community
        self._port = port_number
        self._oid = oid
        self._state = None

    @property
    def name(self):
        return f"PoE Port {self._port}"

    @property
    def is_on(self):
        return self._state == 1

    async def async_turn_on(self, **kwargs):
        await snmp_set(self._host, self._community, self._oid, 1)
        self._state = 1

    async def async_turn_off(self, **kwargs):
        await snmp_set(self._host, self._community, self._oid, 2)
        self._state = 2

    async def async_update(self):
        value = await snmp_get(self._host, self._community, self._oid)
        self._state = int(value)
