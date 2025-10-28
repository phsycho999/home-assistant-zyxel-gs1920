from homeassistant.components.switch import SwitchEntity
from .const import OID_IF_ADMIN_STATUS, OID_POE_POWER_UP

class ZyxelPortSwitch(SwitchEntity):
    def __init__(self, snmp_client, port):
        self.snmp = snmp_client
        self.port = port
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self.snmp.set(f"{OID_IF_ADMIN_STATUS}.{self.port}", 1)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self.snmp.set(f"{OID_IF_ADMIN_STATUS}.{self.port}", 2)
        self._is_on = False
        self.async_write_ha_state()

class ZyxelPoESwitch(SwitchEntity):
    def __init__(self, snmp_client, port):
        self.snmp = snmp_client
        self.port = port
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self.snmp.set(f"{OID_POE_POWER_UP}.{self.port}", 1)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self.snmp.set(f"{OID_POE_POWER_UP}.{self.port}", 2)
        self._is_on = False
        self.async_write_ha_state()
