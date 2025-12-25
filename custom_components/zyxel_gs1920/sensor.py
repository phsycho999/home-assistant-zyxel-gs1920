from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNAVAILABLE
from .const import (
    DOMAIN,
    DEFAULT_PORTS,
    OID_IF_OPER_STATUS,
    OID_POE_STATUS,
    OID_POE_CONSUMPTION,
    OID_POE_CLASSIFICATION,
)

async def async_setup_entry(hass, entry, async_add_entities):
    snmp = hass.data[DOMAIN][entry.entry_id]

    sensors = []
    for port in range(1, DEFAULT_PORTS + 1):
        sensors.extend([
            ZyxelPortSensor(snmp, entry.entry_id, port, "Port Status", OID_IF_OPER_STATUS),
            ZyxelPortSensor(snmp, entry.entry_id, port, "PoE Status", OID_POE_STATUS),
            ZyxelPortSensor(snmp, entry.entry_id, port, "PoE Consumption", OID_POE_CONSUMPTION),
            ZyxelPortSensor(snmp, entry.entry_id, port, "PoE Class", OID_POE_CLASSIFICATION),
        ])
    async_add_entities(sensors)


class ZyxelPortSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, snmp, entry_id, port, name, oid):
        self.snmp = snmp
        self.port = port
        self.oid = f"{oid}.{port}"
        self._attr_name = f"{name} {port}"
        self._attr_unique_id = f"{entry_id}_{name.replace(' ', '_').lower()}_{port}"
        self._state = None

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": f"Zyxel GS1920 Port {self.port}",
            "manufacturer": "Zyxel",
            "model": "GS1920",
        }

    async def async_update(self):
        try:
            value = await self.snmp.get(self.oid)
            if value is None:
                self._state = STATE_UNAVAILABLE
            else:
                self._state = int(value)
        except Exception:
            self._state = STATE_UNAVAILABLE
