from homeassistant.components.switch import SwitchEntity
from .snmp import set_snmpv3, get_snmpv3
from .const import DEFAULT_PORTS

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    snmp_user = entry.data["snmp_user"]
    auth_protocol = entry.data["auth_protocol"]
    auth_password = entry.data["auth_password"]
    priv_protocol = entry.data["priv_protocol"]
    priv_password = entry.data["priv_password"]

    switches = []

    for port in range(1, DEFAULT_PORTS + 1):
        switches.append(ZyxelPortPoESwitch(host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, port))
        switches.append(ZyxelPortAdminSwitch(host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, port))

    async_add_entities(switches)


class ZyxelPortPoESwitch(SwitchEntity):
    """PoE Switch"""

    def __init__(self, host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, port):
        self._host = host
        self._snmp_user = snmp_user
        self._auth_protocol = auth_protocol
        self._auth_password = auth_password
        self._priv_protocol = priv_protocol
        self._priv_password = priv_password
        self._port = port
        self._name = f"Port {port} PoE"
        self._is_on = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        set_snmpv3(self._host, self._snmp_user, self._auth_protocol, self._auth_password,
                   self._priv_protocol, self._priv_password, f"poeOID.{self._port}", 1)
        se
