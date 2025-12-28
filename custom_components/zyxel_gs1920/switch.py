from homeassistant.helpers.entity import ToggleEntity
from .const import DOMAIN
from .snmp import set_poe_port

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    switches = [
        ZyxelPoESwitch(coordinator, index)
        for index in coordinator.data
    ]
    async_add_entities(switches, True)

class ZyxelPoESwitch(ToggleEntity):
    def __init__(self, coordinator, port_index):
        self.coordinator = coordinator
        self.port_index = port_index

    @property
    def name(self):
        return self.coordinator.data[self.port_index]["name"]

    @property
    def is_on(self):
        return self.coordinator.data[self.port_index]["poe"] > 0

    async def async_turn_on(self, **kwargs):
        await set_poe_port(
            self.coordinator.host,
            self.coordinator.user_data,
            self.port_index,
            True
        )
        await self.coordinator.async_refresh()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await set_poe_port(
            self.coordinator.host,
            self.coordinator.user_data,
            self.port_index,
            False
        )
        await self.coordinator.async_refresh()
        self.async_write_ha_state()
