from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, DEFAULT_PORTS
from .snmp import get_ports, get_poe_status

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    username = entry.data["username"]
    auth_key = entry.data.get("auth_key", "")
    priv_key = entry.data.get("priv_key", "")

    ports = await get_ports(host, username, auth_key, priv_key)
    poe = await get_poe_status(host, username, auth_key, priv_key)

    entities = []
    for port, status in ports.items():
        entities.append(ZyxelPortSensor(entry.entry_id, port, status, poe.get(port, False)))
    async_add_entities(entities)

class ZyxelPortSensor(SensorEntity):
    def __init__(self, entry_id, port, status, poe_status):
        self._entry_id = entry_id
        self._port = port
        self._status = status
        self._poe = poe_status
        self._name = f"Port {port}"
        self._unique_id = f"{entry_id}_port_{port}"

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return "on" if self._status else "off"

    @property
    def extra_state_attributes(self):
        return {"poe": self._poe}
