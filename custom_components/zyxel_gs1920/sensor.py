from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([ZyxelSystemNameSensor(coordinator)])


class ZyxelSystemNameSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Zyxel Switch System Name"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = "zyxel_gs1920_sysname"

    @property
    def native_value(self):
        return self.coordinator.data["sys_name"]
