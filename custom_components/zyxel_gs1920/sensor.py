from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for port, info in coordinator.data.items():
        entities.append(ZyxelPoeSensor(coordinator, port))

    async_add_entities(entities)


class ZyxelPoeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, port):
        super().__init__(coordinator)
        self.port = port

    @property
    def name(self):
        return f"{self.coordinator.data[self.port]['name']} PoE"

    @property
    def native_value(self):
        return self.coordinator.data[self.port]["poe"]
