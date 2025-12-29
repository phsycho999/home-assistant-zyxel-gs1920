from homeassistant.helpers.entity import ToggleEntity
from .snmp import set_poe_port

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[entry.entry_id]
    switches = [ZyxelPoESwitch(coordinator, port["index"], port["name"]) for port in coordinator.ports]
    async_add_entities(switches)

class ZyxelPoESwitch(ToggleEntity):
    def __init__(self, coordinator, port_index, name):
        self.coordinator = coordinator
        self.port_index = port_index
        self._name = name
        self._is_on = None

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        port = next((p for p in self.coordinator.ports if p["index"] == self.port_index), None)
        return port["poe"] > 0 if port else False

    async def async_turn_on(self, **kwargs):
        await set_poe_port(self.coordinator.host, self.coordinator.user_data, self.port_index, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await set_poe_port(self.coordinator.host, self.coordinator.user_data, self.port_index, False)
        await self.coordinator.async_request_refresh()
