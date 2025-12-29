from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ZyxelPortAdminSwitch(coordinator)])


class ZyxelPortAdminSwitch(CoordinatorEntity, SwitchEntity):
    _attr_name = "Zyxel Port 1"
    _attr_icon = "mdi:ethernet"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def is_on(self):
        return self.coordinator.data["port1_admin"] == 1

    async def async_turn_on(self, **kwargs):
        await self.coordinator.snmp.set_port_admin(1, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.snmp.set_port_admin(1, False)
        await self.coordinator.async_request_refresh()
