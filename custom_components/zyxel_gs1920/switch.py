from homeassistant.helpers.entity import ToggleEntity
from .const import DOMAIN, DEFAULT_PORTS
from .snmp import set_poe_port

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    username = entry.data["username"]
    auth_key = entry.data.get("auth_key", "")
    priv_key = entry.data.get("priv_key", "")

    switches = [ZyxelPoESwitch(host, username, port, auth_key, priv_key) for port in range(1, DEFAULT_PORTS + 1)]
    async_add_entities(switches)

class ZyxelPoESwitch(ToggleEntity):
    def __init__(self, host, username, port_index, auth_key, priv_key):
        self._host = host
        self._username = username
        self._port_index = port_index
        self._auth_key = auth_key
        self._priv_key = priv_key
        self._is_on = None
        self._name = f"PoE Port {port_index}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = await set_poe_port(self._host, self._username, self._port_index, True, self._auth_key, self._priv_key)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = not await set_poe_port(self._host, self._username, self._port_index, False, self._auth_key, self._priv_key)
        self.async_write_ha_state()
