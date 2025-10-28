from homeassistant.core import HomeAssistant
from .sensor import async_setup_sensors
from .switch import async_setup_switches

async def async_setup_entry(hass: HomeAssistant, entry):
    host = entry.data["host"]
    community = entry.data.get("community", "public")
    port = entry.data.get("port", 161)

    # Sensoren
    await async_setup_sensors(hass, host, community)

    # Switches
    await async_setup_switches(hass, host, community)

    return True
