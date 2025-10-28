from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .sensor import async_setup_sensors
from .switch import ZyxelPortSwitch, ZyxelPoESwitch
from .snmp import SNMPClient

PLATFORMS = ["sensor", "switch"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    host = entry.data["host"]
    community = entry.data["community"]

    snmp_client = SNMPClient(host, community)

    # Sensoren erstellen
    await async_setup_sensors(hass, host, community)

    # Switches erstellen
    switches = []
    for port in range(1, 25):
        switches.append(ZyxelPortSwitch(snmp_client, port))
        switches.append(ZyxelPoESwitch(snmp_client, port))
    hass.async_create_task(
        hass.helpers.entity_platform.async_add_entities(switches)
    )

    return True
