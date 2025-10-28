from .const import DOMAIN
from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import async_setup_switches
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    host = entry.data.get("host")
    snmp_version = entry.data.get("snmp_version", "2c")
    community = entry.data.get("community", "public")
    user = entry.data.get("user")
    auth_key = entry.data.get("auth_key")
    priv_key = entry.data.get("priv_key")

    snmp_client = SNMPClient(host, community, snmp_version, user, auth_key, priv_key)

    # Sensoren
    hass.async_create_task(
        async_setup_sensors(hass, snmp_client, hass.helpers.entity_platform.async_add_entities)
    )

    # Switches
    hass.async_create_task(
        async_setup_switches(hass, snmp_client, hass.helpers.entity_platform.async_add_entities)
    )

    return True

# Damit HA weiß, dass eine Config Flow existiert
async_setup = async_setup_entry
