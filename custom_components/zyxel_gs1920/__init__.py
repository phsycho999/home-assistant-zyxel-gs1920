"""Zyxel GS1920 integration"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .sensor import async_setup_sensors
from .switch import async_setup_switches

DOMAIN = "zyxel_gs1920"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Zyxel GS1920 from a config entry."""
    host = entry.data["host"]
    community = entry.data["community"]

    await async_setup_sensors(hass, host, community)
    await async_setup_switches(hass, host, community)
    return True
