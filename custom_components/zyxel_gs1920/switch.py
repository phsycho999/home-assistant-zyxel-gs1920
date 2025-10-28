from homeassistant.components.switch import SwitchEntity
from .snmp import snmp_set, snmp_get

PORT_ADMIN_STATUS_OID = "1.3.6.1.4.1.890.1.61.2.1.1"
POE_ADMIN_STATUS_OID = "1.3.6.1.4.1.890.1.59.2.1.1"

class ZyxelPortSwitch(SwitchEntity):
    def __init__(self, host, community, port_index, name, oid):
        self._host = host
        self._community = community
        self._port_index = port_index
        self._attr_name = name
        self._oid = f"{oid}.{port_index}"
        self._attr_is_on = None

    @property
    def is_on(self):
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        await snmp_set(self._host, self._oid, 1, self._community)
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        await snmp_set(self._host, self._oid, 2, self._community)
        self._attr_is_on = False

    async def async_update(self):
        value = await snmp_get(self._host, self._oid, self._community)
        self._attr_is_on = bool(value)

async def async_setup_switches(hass, host, community):
    switches = []
    for i in range(1, 25):
        switches.append(ZyxelPortSwitch(host, community, i, f"Port {i} Switch", PORT_ADMIN_STATUS_OID))
        switches.append(ZyxelPortSwitch(host, community, i, f"PoE Port {i} Switch", POE_ADMIN_STATUS_OID))

    hass.async_create_task(hass.helpers.entity_platform.async_add_entities(switches))
