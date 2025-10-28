from homeassistant.components.sensor import SensorEntity
from .snmp import snmp_get
from .const import OID_IF_ADMIN_STATUS, OID_POE_STATUS, OID_POE_CLASS

PORT_ADMIN_STATUS_OID = OID_IF_ADMIN_STATUS
POE_ADMIN_STATUS_OID = OID_POE_STATUS
POE_CONSUMPTION_OID = OID_POE_STATUS
POE_CLASSIFICATION_OID = OID_POE_CLASS

class ZyxelPortSensor(SensorEntity):
    def __init__(self, host, community, port_index, name, oid):
        self._host = host
        self._community = community
        self._port_index = port_index
        self._attr_name = name
        self._oid = f"{oid}.{port_index}"
        self._attr_native_value = None

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        self._attr_native_value = await snmp_get(self._host, self._oid, self._community)

async def async_setup_sensors(hass, host, community):
    sensors = []
    for i in range(1, 25):
        sensors.append(ZyxelPortSensor(host, community, i, f"Port {i} Admin Status", PORT_ADMIN_STATUS_OID))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Status", POE_ADMIN_STATUS_OID))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Consumption", POE_CONSUMPTION_OID))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Class", POE_CLASSIFICATION_OID))

    hass.async_create_task(hass.helpers.entity_platform.async_add_entities(sensors))
