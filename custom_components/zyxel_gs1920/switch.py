from homeassistant.components.switch import SwitchEntity
from .snmp import set_snmp, get_snmp
from .const import DEFAULT_PORTS

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    community = entry.data["community"]
    switches = []

    for port in range(1, DEFAULT_PORTS + 1):
        switches.append(ZyxelPortPoESwitch(host, port, community))
        switches.append(ZyxelPortAdminSwitch(host, port, community))

    async_add_entities(switches)

class ZyxelPortPoESwitch(SwitchEntity):
    """PoE Switch"""

    def __init__(self, host, port, community):
        self._host = host
        self._port = port
        self._community = community
        self._name = f"Port {port} PoE"
        self._is_on = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        set_snmp(self._host, self._community, f"poeOID.{self._port}", 1)
        self._is_on = True
        self.async_write_ha_state()

    def turn_off(self, **kwargs):
        set_snmp(self._host, self._community, f"poeOID.{self._port}", 2)
        self._is_on = False
        self.async_write_ha_state()

class ZyxelPortAdminSwitch(SwitchEntity):
    """Port Enable/Disable"""

    def __init__(self, host, port, community):
        self._host = host
        self._port = port
        self._community = community
        self._name = f"Port {port} Admin"
        self._is_on = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        set_snmp(self._host, self._community, f"portAdminOID.{self._port}", 1)
        self._is_on = True
        self.async_write_ha_state()

    def turn_off(self, **kwargs):
        set_snmp(self._host, self._community, f"portAdminOID.{self._port}", 2)
        self._is_on = False
        self.async_write_ha_state()
