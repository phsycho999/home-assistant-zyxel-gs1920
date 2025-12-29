from .const import DOMAIN, PLATFORMS

async def async_setup(hass, config):
    """Integration minimal setup."""
    return True

async def async_setup_entry(hass, entry):
    """Set up the integration from a config entry."""
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True
