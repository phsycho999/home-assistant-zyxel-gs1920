from homeassistant.components.switch import SwitchEntity
from .const import OID_IF_ADMIN_STATUS, OID_POE_POWER_UP
from .snmp import snmp_set

class ZyxelPortSwitch(SwitchEntity):
    def __init__(self, host, community, port_id):
        self.host = host
        self.community = community
        self.port_id = port_id
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await snmp_set(self.host, OID_IF_ADMIN_STATUS + f".{self.port_id}", 1, self.community)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await snmp_set(self.host, OID_IF_ADMIN_STATUS + f".{self.port_id}", 2, self.community)
        self._is_on = False
        self.async_write_ha_state()

class ZyxelPoESwitch(SwitchEntity):
    def __init__(self, host, community, port_id):
        self.host = host
        self.community = community
        self.port_id = port_id
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await snmp_set(self.host, OID_POE_POWER_UP + f".{self.port_id}", 1, self.community)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await snmp_set(self.host, OID_POE_POWER_UP + f".{self.port_id}", 2, self.community)
        self._is_on = False
        self.async_write_ha_state()

async def async_setup_switches(hass, host, community):
    switches = []
    for i in range(1, 25):
        switches.append(ZyxelPortSwitch(host, community, i))
        switches.append(ZyxelPoESwitch(host, community, i))

    hass.async_create_task(hass.helpers.entity_platform.async_add_entities(switches))
