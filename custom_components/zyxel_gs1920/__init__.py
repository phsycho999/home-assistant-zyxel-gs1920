from homeassistant.core import HomeAssistant

DOMAIN = "zyxel_gs1920"

async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices=None):
    """Set up Zyxel GS1920 from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload Zyxel GS1920 config entry."""
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)
    return True
