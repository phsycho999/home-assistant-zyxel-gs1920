from homeassistant.components.sensor import SensorEntity
from .snmp import SNMPClient

PORT_ADMIN_STATUS_OID = "1.3.6.1.4.1.890.1.61.2.1.1"
POE_ADMIN_STATUS_OID = "1.3.6.1.4.1.890.1.59.2.1.1"
POE_CONSUMPTION_OID = "1.3.6.1.4.1.890.1.59.2.1.1.1"
POE_CLASSIFICATION_OID = "1.3.6.1.4.1.890.1.59.2.1.1.4"

class ZyxelPortSensor(SensorEntity):
    def __init__(self, host, community, port_index, name, oid):
        self._host = host
        self._community = community
        self._port_index = port_index
        self._attr_name = name
        self._oid = f"{oid}.{port_index}"
        self._attr_native_value = None
        self.snmp = SNMPClient(host, community)

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        self._attr_native_value = await self.snmp.get(self._oid)

async def async_setup_sensors(hass, host, community):
    sensors = []
    for i in range(1, 25):
        sensors.append(ZyxelPortSensor(host, community, i, f"Port {i} Admin Status", PORT_ADMIN_STATUS_OID))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Status", POE_ADMIN_STATUS_OID))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Consumption", POE_CONSUMPTION_OID))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Class", POE_CLASSIFICATION_OID))

    hass.async_create_task(hass.helpers.entity_platform.async_add_entities(sensors))
