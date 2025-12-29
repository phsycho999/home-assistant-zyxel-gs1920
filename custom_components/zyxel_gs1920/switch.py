from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .snmp import set_poe


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for port in coordinator.data:
        entities.append(ZyxelPoeSwitch(coordinator, port))

    async_add_entities(entities)


class ZyxelPoeSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, port):
        super().__init__(coordinator)
        self.port = port

    @property
    def name(self):
        return f"{self.coordinator.data[self.port]['name']} PoE Switch"

    @property
    def is_on(self):
        return self.coordinator.data[self.port]["poe"] == 1

    async def async_turn_on(self, **kwargs):
        await set_poe(self.coordinator.host, self.coordinator.user, self.port, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await set_poe(self.coordinator.host, self.coordinator.user, self.port, False)
        await self.coordinator.async_request_refresh()
