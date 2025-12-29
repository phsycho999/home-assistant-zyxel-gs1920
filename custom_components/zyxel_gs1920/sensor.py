from homeassistant.helpers.entity import Entity
from .coordinator import ZyxelCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = ZyxelCoordinator(
        hass,
        entry.data["host"],
        entry.data["username"],
        entry.data.get("auth_key"),
        entry.data.get("priv_key")
    )
    await coordinator.async_config_entry_first_refresh()

    sensors = [ZyxelPoESensor(coordinator, port["index"], port["name"]) for port in coordinator.ports]
    async_add_entities(sensors)

class ZyxelPoESensor(Entity):
    def __init__(self, coordinator, port_index, name):
        self.coordinator = coordinator
        self.port_index = port_index
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        port = next((p for p in self.coordinator.ports if p["index"] == self.port_index), None)
        return port["poe_status"] if port else None

    async def async_update(self):
        await self.coordinator.async_request_refresh()
