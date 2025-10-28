"""Zyxel GS1920 integration."""

from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Zyxel GS1920 component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Sensoren und Schalter laden
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "switch"])
    return True
