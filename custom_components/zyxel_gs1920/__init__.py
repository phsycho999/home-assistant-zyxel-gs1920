from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .coordinator import ZyxelCoordinator
from .const import DOMAIN, PLATFORMS

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = ZyxelCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    for platform in PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(entry, platform)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
