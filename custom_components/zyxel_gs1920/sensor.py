from homeassistant.components.sensor import SensorEntity

class ZyxelPoEPowerSensor(SensorEntity):
    """Represents PoE power consumption sensor."""

    def __init__(self, port_data):
        self._port_data = port_data
        self._attr_name = f"Zyxel PoE Power Port {port_data['port']}"
        self._attr_native_value = port_data['power_consumption']

    @property
    def native_unit_of_measurement(self):
        return "mW"

    async def async_update(self):
        # TODO: SNMP Abfrage PoE Power
        self._attr_native_value = self._port_data.get("power_consumption", 0)
