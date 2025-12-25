from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_UNAVAILABLE
from .const import (
    DOMAIN,
    DEFAULT_PORTS,
    OID_IF_ADMIN_STATUS,
    OID_POE_POWER_UP,
)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Zyxel GS1920 switches."""
    snmp = hass.data[DOMAIN][entry.entry_id]

    switches = []
    for port in range(1, DEFAULT_PORTS + 1):
        switches.extend([
            ZyxelPortSwitch(snmp, entry.entry_id, port),
            ZyxelPoESwitch(snmp, entry.entry_id, port),
        ])
    async_add_entities(switches)


class ZyxelBaseSwitch(SwitchEntity):
    _attr_should_poll = True

    def __init__(self, snmp, entry_id, port, name, oid, on_value=1, off_value=2):
        self.snmp = snmp
        self.port = port
        self.oid = f"{oid}.{port}"
        self._attr_name = f"{name} {port}"
        self._attr_unique_id = f"{entry_id}_{name.replace(' ', '_').lower()}_{port}"
        self._is_on = None
        self._on_value = on_value
        self._off_value = off_value

    @property
    def is_on(self):
        return self._is_on

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": f"Zyxel GS1920 Port {self.port}",
            "manufacturer": "Zyxel",
            "model": "GS1920",
        }

    async def async_update(self):
        try:
            value = await self.snmp.get(self.oid)
            if value is None:
                self._is_on = None
            else:
                self._is_on = int(value) == self._on_value
        except Exception:
            self._is_on = None

    async def async_turn_on(self, **kwargs):
        await self.snmp.set(self.oid, self._on_value)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.snmp.set(self.oid, self._off_value)
        self._is_on = False
        self.async_write_ha_state()


class ZyxelPortSwitch(ZyxelBaseSwitch):
    def __init__(self, snmp, entry_id, port):
        super().__init__(snmp, entry_id, port, "Port Admin", OID_IF_ADMIN_STATUS)


class ZyxelPoESwitch(ZyxelBaseSwitch):
    def __init__(self, snmp, entry_id, port):
        super().__init__(snmp, entry_id, port, "PoE Power", OID_POE_POWER_UP)
