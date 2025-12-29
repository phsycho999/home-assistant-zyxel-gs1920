from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ZyxelPortAdminSensor(coordinator)])


class ZyxelPortAdminSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Zyxel Port 1 Admin Status"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def native_value(self):
        return "up" if self.coordinator.data["port1_admin"] == 1 else "down"
