from homeassistant.components.switch import SwitchEntity
from .const import OID_IF_ADMIN_STATUS, OID_POE_POWER_UP

class ZyxelPortSwitch(SwitchEntity):
    def __init__(self, snmp_client, port_id):
        self.snmp = snmp_client
        self.port_id = port_id
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_update(self):
        value = await self.snmp.get(OID_IF_ADMIN_STATUS + f".{self.port_id}")
        self._is_on = value == 1

    async def async_turn_on(self, **kwargs):
        await self.snmp.set(OID_IF_ADMIN_STATUS + f".{self.port_id}", 1)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.snmp.set(OID_IF_ADMIN_STATUS + f".{self.port_id}", 2)
        self._is_on = False
        self.async_write_ha_state()


class ZyxelPoESwitch(SwitchEntity):
    def __init__(self, snmp_client, port_id):
        self.snmp = snmp_client
        self.port_id = port_id
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_update(self):
        value = await self.snmp.get(OID_POE_POWER_UP + f".{self.port_id}")
        self._is_on = value == 1

    async def async_turn_on(self, **kwargs):
        await self.snmp.set(OID_POE_POWER_UP + f".{self.port_id}", 1)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.snmp.set(OID_POE_POWER_UP + f".{self.port_id}", 2)
        self._is_on = False
        self.async_write_ha_state()
