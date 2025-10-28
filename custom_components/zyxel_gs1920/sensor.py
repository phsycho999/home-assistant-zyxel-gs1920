from homeassistant.helpers.entity import Entity
from homeassistant.helpers import entity_platform
from .const import DEFAULT_PORTS, OID_IF_OPER_STATUS, OID_POE_STATUS, OID_POE_CONSUMPTION, OID_POE_CLASSIFICATION

class ZyxelPortSensor(Entity):
    def __init__(self, snmp_client, port_index, name, oid):
        self.snmp = snmp_client
        self.port_index = port_index
        self._attr_name = name
        self.oid = f"{oid}.{port_index}"
        self._state = None

    @property
    def state(self):
        return self._state

    async def async_update(self):
        self._state = await self.snmp.get(self.oid)

async def async_setup_sensors(hass, snmp_client):
    sensors = []
    for i in range(1, DEFAULT_PORTS + 1):
        sensors.append(ZyxelPortSensor(snmp_client, i, f"Port {i} Status", OID_IF_OPER_STATUS))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE {i} Status", OID_POE_STATUS))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE {i} Consumption", OID_POE_CONSUMPTION))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE {i} Class", OID_POE_CLASSIFICATION))

    platform = entity_platform.async_get_current_platform()
    platform.async_add_entities(sensors)
