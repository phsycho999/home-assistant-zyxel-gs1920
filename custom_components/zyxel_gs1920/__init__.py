from .const import DOMAIN, PLATFORMS
from .coordinator import ZyxelGS1920Coordinator


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass, entry):
    coordinator = ZyxelGS1920Coordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
