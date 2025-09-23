from homeassistant.components.sensor import SensorEntity
from .snmp import get_snmpv3
from .const import DEFAULT_PORTS

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    snmp_user = entry.data["username"]
    auth_protocol = "MD5"
    auth_password = entry.data["auth_key"]
    priv_protocol = "DES"
    priv_password = entry.data["priv_key"]

    sensors = []
    for port in range(1, DEFAULT_PORTS + 1):
        sensors.append(ZyxelPortStatus(host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, port))

    async_add_entities(sensors)


class ZyxelPortStatus(SensorEntity):
    """Port Status Sensor"""

    def __init__(self, host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, port):
        self._host = host
        self._snmp_user = snmp_user
        self._auth_protocol = auth_protocol
        self._auth_password = auth_password
        self._priv_protocol = priv_protocol
        self._priv_password = priv_password
        self._port = port
        self._name = f"Port {port} Status"
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        self._state = get_snmpv3(self._host, self._snmp_user, self._auth_protocol,
                                  self._auth_password, self._priv_protocol,
                                  self._priv_password, f"portStatusOID.{self._port}") or "down"
