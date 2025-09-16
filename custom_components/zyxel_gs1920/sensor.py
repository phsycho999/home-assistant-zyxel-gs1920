from homeassistant.components.sensor import SensorEntity
from .snmp import get_snmp
from .const import DEFAULT_PORTS

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    community = entry.data["community"]
    sensors = []

    for port in range(1, DEFAULT_PORTS + 1):
        sensors.append(ZyxelPortStatus(host, port, community))

    async_add_entities(sensors)

class ZyxelPortStatus(SensorEntity):
    """Port Status Sensor"""

    def __init__(self, host, port, community):
        self._host = host
        self._port = port
        self._community = community
        self._name = f"Port {port} Status"
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        # Beispiel: SNMP-Abfrage Port Status
        self._state = get_snmp(self._host, self._community, f"portStatusOID.{self._port}") or "down"
