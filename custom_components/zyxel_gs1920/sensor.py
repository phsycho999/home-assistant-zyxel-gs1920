from homeassistant.components.sensor import SensorEntity
from .snmp import snmp_get
from .const import DEFAULT_PORTS, PORT_ADMIN_STATUS_OID, POE_ADMIN_STATUS_OID, POE_CONSUMPTION_OID, POE_CLASSIFICATION_OID

class ZyxelPortSensor(SensorEntity):
    """Sensor für einen einzelnen Switch-Port."""

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

async def async_setup_sensors(hass, snmp_client):
    sensors = []

    for i in range(1, DEFAULT_PORTS + 1):
        sensors.append(ZyxelPortSensor(snmp_client, i, f"Port {i} Admin Status", PORT_ADMIN_STATUS_OID))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE Port {i} Status", POE_ADMIN_STATUS_OID))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE Port {i} Consumption", POE_CONSUMPTION_OID))
        sensors.append(ZyxelPortSensor(snmp_client, i, f"PoE Port {i} Class", POE_CLASSIFICATION_OID))

    platform = hass.data["zyxel_gs1920"]["platform"]
    platform.async_add_entities(sensors)
