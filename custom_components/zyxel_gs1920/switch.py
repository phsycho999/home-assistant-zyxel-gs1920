from homeassistant.components.switch import SwitchEntity
from .coordinator import ZyxelCoordinator

class ZyxelPortSwitch(SwitchEntity):
    def __init__(self, coordinator, port_number):
        self.coordinator = coordinator
        self.port = port_number
        self._attr_name = f"Port {port_number} POE"
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        await self.coordinator.snmp.set(f"1.3.6.1.2.1.105.1.1.1.3.{self.port}", 1)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.snmp.set(f"1.3.6.1.2.1.105.1.1.1.3.{self.port}", 2)
        self._attr_is_on = False
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._attr_is_on

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["zyxel_gs1920"][entry.entry_id]
    entities = [ZyxelPortSwitch(coordinator, i+1) for i in range(24)]  # 24 Ports
    async_add_entities(entities)
