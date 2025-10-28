from homeassistant.components.sensor import SensorEntity
from .snmp import SNMPClient
from .const import OID_IF_ADMIN_STATUS, OID_POE_POWER_UP, OID_POE_STATUS, OID_POE_CONSUMPTION, OID_POE_CLASSIFICATION

class ZyxelPortSensor(SensorEntity):
    def __init__(self, snmp_client, port_index, name, oid):
        self.snmp = snmp_client
        self.port_index = port_index
        self._attr_name = name
        self._oid = f"{oid}.{port_index}"
        self._attr_native_value = None

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        self._attr_native_value = await self.snmp.get(self._oid)

async def async_setup_sensors(hass, snmp_client, ports=24):
    sensors = []
    for i in range(1, ports+1):
        sensors.append(ZyxelPortSensor(snmp_client, i, f"Port {i} Admin Status", OID_IF_ADMIN_STATUS))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE Port {i} Status", OID_POE_STATUS))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE Port {i} Consumption", OID_POE_CONSUMPTION))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE Port {i} Class", OID_POE_CLASSIFICATION))
    hass.async_create_task(hass.helpers.entity_platform.async_add_entities(sensors))
