from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .snmp import SNMPClient

PLATFORMS = ["sensor", "switch"]

async def async_setup(hass: HomeAssistant, config) -> bool:
    """Empty setup, using config entries only."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Zyxel GS1920 integration from a config entry."""

    # SNMP client erzeugen (wie bisher)
    snmp_client = SNMPClient(
        host=entry.data.get("host"),
        port=entry.data.get("snmp_port", 161),
        version=entry.data.get("snmp_version", "2c"),
        community=entry.data.get("community", "public"),
        user=entry.data.get("user"),
        auth_key=entry.data.get("auth_key"),
        priv_key=entry.data.get("priv_key"),
    )

    # SNMP client in hass.data zentral speichern
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = snmp_client

    # Sensoren und Switches über die Plattformen einrichten
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and its platforms."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
