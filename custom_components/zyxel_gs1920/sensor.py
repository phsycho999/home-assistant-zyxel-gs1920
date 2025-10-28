from homeassistant.components.sensor import SensorEntity
from .const import OID_IF_OPER_STATUS, OID_POE_STATUS, OID_POE_CONSUMPTION, OID_POE_CLASS
from .snmp import snmp_get

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
        # Port Status
        sensors.append(ZyxelPortSensor(host, community, i, f"Port {i} Status", OID_IF_OPER_STATUS))
        # PoE Status
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Status", OID_POE_STATUS))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Consumption", OID_POE_CONSUMPTION))
        sensors.append(ZyxelPortSensor(host, community, i, f"PoE Port {i} Class", OID_POE_CLASS))

    hass.async_create_task(hass.helpers.entity_platform.async_add_entities(sensors))
