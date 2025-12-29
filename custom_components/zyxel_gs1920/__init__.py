"""Zyxel GS1920 Integration."""
from homeassistant.core import HomeAssistant

DOMAIN = "zyxel_gs1920"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Zyxel GS1920 integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
