from homeassistant.components.switch import SwitchEntity
from .const import DEFAULT_PORTS, OID_IF_ADMIN_STATUS, OID_POE_POWER_UP

class ZyxelPortSwitch(SwitchEntity):
    def __init__(self, snmp_client, port_index):
        self.snmp = snmp_client
        self.port_index = port_index
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self.snmp.set(f"{OID_IF_ADMIN_STATUS}.{self.port_index}", 1)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.snmp.set(f"{OID_IF_ADMIN_STATUS}.{self.port_index}", 2)
        self._is_on = False
        self.async_write_ha_state()

class ZyxelPoESwitch(SwitchEntity):
    def __init__(self, snmp_client, port_index):
        self.snmp = snmp_client
        self.port_index = port_index
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self.snmp.set(f"{OID_POE_POWER_UP}.{self.port_index}", 1)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.snmp.set(f"{OID_POE_POWER_UP}.{self.port_index}", 2)
        self._is_on = False
        self.async_write_ha_state()

async def async_setup_switches(hass, snmp_client, async_add_entities):
    switches = []
    for i in range(1, DEFAULT_PORTS + 1):
        switches.append(ZyxelPortSwitch(snmp_client, i))
        switches.append(ZyxelPoESwitch(snmp_client, i))
    async_add_entities(switches)
