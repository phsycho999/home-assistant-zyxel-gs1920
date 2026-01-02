from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, PORT_COUNT, POE_PORT_OID


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for port in range(1, PORT_COUNT + 1):
        entities.append(ZyxelPoeSwitch(coordinator, port))

    async_add_entities(entities)


class ZyxelPoeSwitch(SwitchEntity):
    def __init__(self, coordinator, port):
        self.coordinator = coordinator
        self.port = port
        self._attr_name = f"PoE Port {port}"
        self._attr_unique_id = f"zyxel_gs1920_poe_{port}"

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, "zyxel_gs1920")},
            name="Zyxel GS1920",
            manufacturer="Zyxel",
            model="GS1920",
        )

    @property
    def is_on(self):
        oid = f"{POE_PORT_OID}.{self.port}"
        return self.coordinator.snmp.get(oid) == 1

    async def async_turn_on(self, **kwargs):
        oid = f"{POE_PORT_OID}.{self.port}"
        await self.coordinator.snmp.set(oid, 1)

    async def async_turn_off(self, **kwargs):
        oid = f"{POE_PORT_OID}.{self.port}"
        await self.coordinator.snmp.set(oid, 2)
