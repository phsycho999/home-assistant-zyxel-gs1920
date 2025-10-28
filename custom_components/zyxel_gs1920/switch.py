from homeassistant.components.switch import SwitchEntity

class ZyxelPortSwitch(SwitchEntity):
    """Represents a physical port switch."""

    def __init__(self, port_data):
        self._port_data = port_data
        self._attr_name = f"Zyxel Port {port_data['port']}"
        self._attr_is_on = port_data['enabled']

    @property
    def is_on(self):
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        # TODO: SNMP Befehl für Port ON
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        # TODO: SNMP Befehl für Port OFF
        self._attr_is_on = False
        self.async_write_ha_state()

class ZyxelPoESwitch(SwitchEntity):
    """Represents a PoE switchable port."""

    def __init__(self, port_data):
        self._port_data = port_data
        self._attr_name = f"Zyxel PoE Port {port_data['port']}"
        self._attr_is_on = port_data['enabled']

    @property
    def is_on(self):
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        # TODO: SNMP Befehl PoE ON
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        # TODO: SNMP Befehl PoE OFF
        self._attr_is_on = False
        self.async_write_ha_state()
