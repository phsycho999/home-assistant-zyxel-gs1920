from homeassistant.components.sensor import SensorEntity
from .const import OID_IF_OPER_STATUS, OID_POE_STATUS, OID_POE_CONSUMPTION, OID_POE_CLASSIFICATION

class ZyxelPortSensor(SensorEntity):
    def __init__(self, snmp_client, port, name, oid):
        self.snmp = snmp_client
        self.port = port
        self._attr_name = name
        self.oid = f"{oid}.{port}"
        self._attr_native_value = None

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        self._attr_native_value = await self.snmp.get(self.oid)

async def async_setup_sensors(hass, snmp_client):
    sensors = []
    for port in range(1, 25):
        sensors.append(ZyxelPortSensor(snmp_client, port, f"Port {port} Status", OID_IF_OPER_STATUS))
        sensors.append(ZyxelPortSensor(snmp_client, port, f"PoE {port} Status", OID_POE_STATUS))
        sensors.append(ZyxelPortSensor(snmp_client, port, f"PoE {port} Consumption", OID_POE_CONSUMPTION))
        sensors.append(ZyxelPortSensor(snmp_client, port, f"PoE {port} Class", OID_POE_CLASSIFICATION))

    hass.async_create_task(
        hass.helpers.entity_platform.async_add_entities(sensors)
    )
