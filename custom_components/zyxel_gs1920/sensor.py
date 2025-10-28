from homeassistant.helpers.entity import SensorEntity
from .snmp import snmp_get

class ZyxelPoEPowerSensor(SensorEntity):
    """PoE-Verbrauch pro Port als Sensor."""

    def __init__(self, host, community, port_number, oid, name):
        self._host = host
        self._community = community
        self._port = port_number
        self._oid = oid
        self._state = None
        self._name = name

    @property
    def name(self):
        return f"{self._name} {self._port}"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        value = await snmp_get(self._host, self._community, self._oid)
        self._state = int(value)
