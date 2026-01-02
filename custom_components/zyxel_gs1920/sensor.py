from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ZyxelSysDescrSensor(coordinator)])


class ZyxelSysDescrSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Zyxel System Description"
    _attr_icon = "mdi:switch"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_sysdescr"

    @property
    def native_value(self):
        return self.coordinator.data
