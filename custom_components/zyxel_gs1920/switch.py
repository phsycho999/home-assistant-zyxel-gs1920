from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    switches = []

    # Beispiel: 24 Ports
    for port in range(1, 25):
        switches.append(ZyxelPortSwitch(coordinator, port))

    async_add_entities(switches)

class ZyxelPortSwitch(SwitchEntity):
    def __init__(self, coordinator, port_index):
        self.coordinator = coordinator
        self.port_index = port_index
        self._attr_name = f"PoE Port {port_index}"
        self._attr_is_on = False

    @property
    def available(self):
        return True

    async def async_turn_on(self, **kwargs):
        await self.coordinator.snmp.set_poe(self.port_index, True)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.snmp.set_poe(self.port_index, False)
        self._attr_is_on = False
        self.async_write_ha_state()
