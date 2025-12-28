from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from .snmp import get_ports, get_poe_status, create_user_data

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    username = entry.data["username"]
    auth_key = entry.data.get("auth_key")
    priv_key = entry.data.get("priv_key")

    user_data = create_user_data(username, auth_key, priv_key)
    ports = await get_ports(host, user_data)
    sensors = [ZyxelPoESensor(host, user_data, port["index"], port["name"]) for port in ports]

    async_add_entities(sensors)

class ZyxelPoESensor(Entity):
    def __init__(self, host, user_data, port_index, name):
        self._host = host
        self._user_data = user_data
        self._port_index = port_index
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        self._state = await get_poe_status(self._host, self._user_data, self._port_index)
