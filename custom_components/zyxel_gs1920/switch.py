from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


PORT1_ADMIN_OID = "1.3.6.1.2.1.2.2.1.7.1"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ZyxelPort1Switch(coordinator)])


class ZyxelPort1Switch(CoordinatorEntity, SwitchEntity):
    _attr_name = "Zyxel Port 1"
    _attr_unique_id = "zyxel_gs1920_port1"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def is_on(self):
        # optional: echten Status abfragen
        return True

    async def async_turn_on(self, **kwargs):
        await self.coordinator.snmp.set(PORT1_ADMIN_OID, 1)

    async def async_turn_off(self, **kwargs):
        await self.coordinator.snmp.set(PORT1_ADMIN_OID, 2)
