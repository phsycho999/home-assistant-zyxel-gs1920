from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .snmp import SNMPClient

PLATFORMS = ["sensor", "switch"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Standard setup, leer da Config Flow verwendet wird."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup aus Config Flow."""
    host = entry.data["host"]
    snmp_version = entry.data.get("snmp_version", "2c")

    if snmp_version == "2c":
        community = entry.data.get("community", "public")
        snmp_client = SNMPClient(host, community)
    else:
        snmp_client = SNMPClient(
            host,
            user=entry.data.get("username"),
            auth_protocol=entry.data.get("auth_protocol"),
            auth_key=entry.data.get("auth_key"),
            priv_protocol=entry.data.get("priv_protocol"),
            priv_key=entry.data.get("priv_key")
        )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = snmp_client

    # Plattformen laden
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unloading a config entry."""
    for platform in PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(entry, platform)

    hass.data[DOMAIN].pop(entry.entry_id)
    return True
