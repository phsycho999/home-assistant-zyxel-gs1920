from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .sensor import async_setup_sensors
from .switch import ZyxelPortSwitch, ZyxelPoESwitch
from .snmp import SNMPClient

PLATFORMS = ["sensor", "switch"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration (deprecated, config_flow used)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Zyxel GS1920 from a config entry."""
    host = entry.data["host"]
    snmp_version = entry.data.get("snmp_version", "2c")

    if snmp_version == "2c":
        community = entry.data.get("community", "public")
        snmp_client = SNMPClient(host, community)
    else:
        snmp_client = SNMPClient(
            host,
            user=entry.data.get("username"),
            auth_protocol=entry.data.get("auth_protocol"),
            auth_key=entry.data.get("auth_key"),
            priv_protocol=entry.data.get("priv_protocol"),
            priv_key=entry.data.get("priv_key")
        )

    # Setup sensors
    await async_setup_sensors(hass, snmp_client)

    # Setup switches
    switches = []
    for port in range(1, 25):
        switches.append(ZyxelPortSwitch(snmp_client, port))
        switches.append(ZyxelPoESwitch(snmp_client, port))

    hass.async_create_task(
        hass.helpers.entity_platform.async_add_entities(switches)
    )

    return True
