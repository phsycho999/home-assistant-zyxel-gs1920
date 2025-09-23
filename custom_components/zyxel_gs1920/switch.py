from homeassistant.components.switch import SwitchEntity
from .snmp import set_snmpv3, get_snmpv3
from .const import DEFAULT_PORTS

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    snmp_user = entry.data["username"]
    auth_protocol = "MD5"
    auth_password = entry.data["auth_key"]
    priv_protocol = "DES"
    priv_password = entry.data["priv_key"]

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
        self._is_on = True

    def turn_off(self, **kwargs):
        set_snmpv3(self._host, self._snmp_user, self._auth_protocol, self._auth_password,
                    self._priv_protocol, self._priv_password, f"poeOID.{self._port}", 2)
        self._is_on = False


class ZyxelPortAdminSwitch(SwitchEntity):
    """Admin Enable/Disable Switch"""

    def __init__(self, host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, port):
        self._host = host
        self._snmp_user = snmp_user
        self._auth_protocol = auth_protocol
        self._auth_password = auth_password
        self._priv_protocol = priv_protocol
        self._priv_password = priv_password
        self._port = port
        self._name = f"Port {port} Admin"
        self._is_on = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        set_snmpv3(self._host, self._snmp_user, self._auth_protocol, self._auth_password,
                    self._priv_protocol, self._priv_password, f"adminOID.{self._port}", 1)
        self._is_on = True

    def turn_off(self, **kwargs):
        set_snmpv3(self._host, self._snmp_user, self._auth_protocol, self._auth_password,
                    self._priv_protocol, self._priv_password, f"adminOID.{self._port}", 2)
        self._is_on = False
