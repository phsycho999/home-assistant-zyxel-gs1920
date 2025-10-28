import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Zyxel GS1920 from a config entry."""
    # Lazy Imports
    from .switch import ZyxelPortSwitch, ZyxelPoESwitch
    from .sensor import ZyxelPoEPowerSensor

    # Hier SNMP-Verbindung aufbauen
    host = entry.data.get("host")
    community = entry.data.get("community", "public")

    hass.data.setdefault("zyxel_gs1920", {})[entry.entry_id] = {
        "host": host,
        "community": community,
        "ports": {},  # Platzhalter für Port-Daten
    }

    # Ports und Sensoren initialisieren
    tasks = []
    for port_id in range(1, 25):
        port_data = {"port": port_id, "enabled": True, "power_consumption": 0}

        tasks.append(ZyxelPortSwitch(port_data))
        tasks.append(ZyxelPoESwitch(port_data))
        tasks.append(ZyxelPoEPowerSensor(port_data))

    # Komponenten registrieren
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, platform) for platform in PLATFORMS]
        )
    )
    if unload_ok:
        hass.data["zyxel_gs1920"].pop(entry.entry_id)
    return unload_ok
