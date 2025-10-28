from homeassistant.core import HomeAssistant
from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import async_setup_switches
from .const import DOMAIN, CONF_HOST, CONF_COMMUNITY, CONF_SNMP_VERSION, CONF_USER, CONF_AUTH_KEY, CONF_PRIV_KEY

async def async_setup_entry(hass: HomeAssistant, entry):
    host = entry.data[CONF_HOST]
    snmp_version = entry.data.get(CONF_SNMP_VERSION, "2c")
    community = entry.data.get(CONF_COMMUNITY, "public")
    user = entry.data.get(CONF_USER)
    auth_key = entry.data.get(CONF_AUTH_KEY)
    priv_key = entry.data.get(CONF_PRIV_KEY)

    snmp_client = SNMPClient(host, snmp_version, community, user, auth_key, priv_key)

    await async_setup_sensors(hass, snmp_client)
    await async_setup_switches(hass, snmp_client)

    return True
