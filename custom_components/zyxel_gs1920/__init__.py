from homeassistant.core import HomeAssistant
from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import async_setup_switches
from .const import CONF_HOST, CONF_COMMUNITY, CONF_SNMP_VERSION, CONF_USER, CONF_AUTH_KEY, CONF_PRIV_KEY

async def async_setup_entry(hass: HomeAssistant, entry):
    # Mapping direkt benutzen
    host = entry.get(CONF_HOST)
    snmp_version = entry.get(CONF_SNMP_VERSION, "2c")
    community = entry.get(CONF_COMMUNITY, "public")
    user = entry.get(CONF_USER)
    auth_key = entry.get(CONF_AUTH_KEY)
    priv_key = entry.get(CONF_PRIV_KEY)

    snmp_client = SNMPClient(host, community, snmp_version, user, auth_key, priv_key)
    hass.data.setdefault("zyxel_gs1920", {})[entry.entry_id] = snmp_client

    # Sensoren & Switches
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "switch"])
    return True
