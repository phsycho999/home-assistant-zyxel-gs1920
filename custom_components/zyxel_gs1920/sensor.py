from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        ZyxelPoESensor(coordinator, index)
        for index in coordinator.data
    ]
    async_add_entities(sensors, True)

class ZyxelPoESensor(Entity):
    def __init__(self, coordinator, port_index):
        self.coordinator = coordinator
        self.port_index = port_index

    @property
    def name(self):
        return self.coordinator.data[self.port_index]["name"]

    @property
    def state(self):
        return self.coordinator.data[self.port_index]["poe"]

    async def async_update(self):
        await self.coordinator.async_refresh()
