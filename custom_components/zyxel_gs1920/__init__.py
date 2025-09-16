"""Zyxel GS1920 integration."""

from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Zyxel GS1920 component."""
    hass.data.setdefault(DOMAIN, {})
    return True
