from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import async_setup_switches

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup the integration (not used with config flow)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Zyxel GS1920 from a config entry."""
    data = entry.data
    snmp_client = SNMPClient(
        host=data.get("host"),
        community=data.get("community"),
        snmp_version=data.get("snmp_version"),
        user=data.get("user"),
        auth_key=data.get("auth_key"),
        priv_key=data.get("priv_key")
    )

    # Sensoren und Switches setzen
    await async_setup_sensors(hass, snmp_client)
    await async_setup_switches(hass, snmp_client)
    return True
