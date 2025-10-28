from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import async_setup_switches
from homeassistant.core import HomeAssistant

async def async_setup_entry(hass: HomeAssistant, entry):
    host = entry.get("host")
    snmp_version = entry.get("snmp_version", "2c")
    community = entry.get("community", "public")
    user = entry.get("user")
    auth_key = entry.get("auth_key")
    priv_key = entry.get("priv_key")

    snmp_client = SNMPClient(host, community, snmp_version, user, auth_key, priv_key)

    # Sensoren
    await async_setup_sensors(hass, snmp_client, hass.helpers.entity_platform.async_add_entities)

    # Switches
    await async_setup_switches(hass, snmp_client, hass.helpers.entity_platform.async_add_entities)

    return True

async_setup = async_setup_entry
