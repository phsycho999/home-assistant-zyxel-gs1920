from homeassistant.helpers.entity import Entity
from .coordinator import ZyxelCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: ZyxelCoordinator = hass.data[entry.entry_id]
    sensors = []
    for port in coordinator.ports:
        sensors.append(ZyxelPoESensor(coordinator, port["index"], port["name"]))
    async_add_entities(sensors)

class ZyxelPoESensor(Entity):
    def __init__(self, coordinator, port_index, name):
        self.coordinator = coordinator
        self.port_index = port_index
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        port = next((p for p in self.coordinator.ports if p["index"] == self.port_index), None)
        return port["poe"] if port else None

    async def async_update(self):
        await self.coordinator.async_request_refresh()
