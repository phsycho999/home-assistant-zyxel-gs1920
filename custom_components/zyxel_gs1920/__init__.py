from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .coordinator import ZyxelCoordinator

DOMAIN = "zyxel_gs1920"

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup the integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up switch from a config entry."""
    coordinator = ZyxelCoordinator(hass, entry)
    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Hier könnten Platformen geladen werden, z.B. sensor/switch
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
