from homeassistant.helpers.entity import ToggleEntity
from .coordinator import ZyxelCoordinator
from .snmp import set_poe_port

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = ZyxelCoordinator(
        hass,
        entry.data["host"],
        entry.data["username"],
        entry.data.get("auth_key"),
        entry.data.get("priv_key")
    )
    await coordinator.async_config_entry_first_refresh()

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
        return bool(port["poe_status"]) if port else None

    async def async_turn_on(self, **kwargs):
        port_index = self.port_index
        await set_poe_port(self.coordinator._host, self.coordinator._user_data, port_index, True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        port_index = self.port_index
        await set_poe_port(self.coordinator._host, self.coordinator._user_data, port_index, False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
